# Standard imports
import os
import json
import pandas as pd
from datetime import datetime

# Django imports
from django.db.models import Max
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Local imports
from core import settings
from .permissions import IsOwnerOrReadOnly
from timetables.models import Timetable, Unit, PendingTransaction, Subscription
from .genetic_algoritm import generate_timetable, double_check_timetable
from django_daraja.mpesa.core import MpesaClient  # type: ignore

# ✅ View to retrieve the subscription details of the authenticated user
class SubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        subscription = Subscription.objects.get(user=request.user)
        response_data = {
            'status': subscription.status,
            'tier': subscription.tier,
        }
        return Response(response_data, status=status.HTTP_200_OK)

# ✅ View to retrieve unit-related statistics for the authenticated user
class UnitsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        units = Unit.objects.filter(user=request.user)
        unique_batch_ids = units.exclude(batch_id=None).values_list('batch_id', flat=True).distinct()
        batch_count = len(unique_batch_ids)
        return Response({'batch_count': batch_count}, status=status.HTTP_200_OK)

# ✅ View to initiate M-Pesa payment for subscription
class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        number = request.data.get('phone_number')
        amnt = request.data.get('amount')

        # Initialize M-Pesa client and prepare transaction details
        cl = MpesaClient()
        amount = int(amnt)
        callback_url = f"{settings.NGROK_URL}/api/v1/mpesa/callback/"
        response = cl.stk_push(number, amount, 'reference', 'Description', callback_url)

        # Handle the response from M-Pesa
        response_data = response.json() if hasattr(response, 'json') else dict(response)
        merchant_request_id = response_data.get("MerchantRequestID")
        if not merchant_request_id:
            return Response({"error": "Failed to get transaction ID"}, status=400)

        # Save transaction for future verification
        PendingTransaction.objects.create(
            user=user, phone_number=number, amount=amount, transaction_id=merchant_request_id
        )

        return HttpResponse(response)

# ✅ Callback view to handle M-Pesa payment confirmation from Safaricom
@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        raw_data = request.body.decode('utf-8')
        if not raw_data.strip():
            return JsonResponse({"error": "Empty request body"}, status=400)

        try:
            data = json.loads(raw_data)
            transaction_id = data.get("Body", {}).get("stkCallback", {}).get("MerchantRequestID", None)
            result_code = data.get("Body", {}).get("stkCallback", {}).get("ResultCode", None)

            if not transaction_id:
                return JsonResponse({"error": "Transaction ID missing"}, status=400)

            pending_transaction = PendingTransaction.objects.filter(transaction_id=transaction_id).first()
            if not pending_transaction:
                return JsonResponse({"error": "Transaction not found"}, status=404)

            if result_code == 0:
                # Mark user as subscribed and update subscription record
                subscription = Subscription.objects.get(user=pending_transaction.user)
                subscription.amount = pending_transaction.amount
                subscription.status = "paid"
                subscription.tier = "Premium"
                subscription.save()
                pending_transaction.delete()
                return JsonResponse({"message": "Subscription successfully created"}, status=200)

            return JsonResponse({"error": "Payment failed"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON received"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

# ✅ View to fetch details of a specific timetable entry
class TimetableDataView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, rowId, format=None):
        timetable = Timetable.objects.get(id=rowId, user=request.user)
        return Response({
            'id': timetable.id,
            'name': timetable.name,
            'unit_code': timetable.unit_code,
            'unit_name': timetable.unit_name,
            'day': timetable.day,
            'start_time': timetable.start_time,
            'end_time': timetable.end_time,
            'lecturer': timetable.lecturer,
            'campus': timetable.campus,
            'mode_of_study': timetable.mode_of_study,
            'lecture_room': timetable.lecture_room,
            'group': timetable.group,
        }, status=status.HTTP_200_OK)

# ✅ View to return recent timetable batch names (used in frontend dropdowns)
class TimetableNameView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, format=None):
        timetables = (
            Timetable.objects
            .filter(user=request.user)
            .values('batch_id', 'name')
            .annotate(latest_created_at=Max('created_at'))
            .order_by('-latest_created_at')
        )
        response_data = [{'batch_id': t['batch_id'], 'name': t['name']} for t in timetables]
        return Response(response_data, status=status.HTTP_200_OK)

# ✅ View to get all timetable sessions for a specific batch
class TimetableView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, batch_id, format=None):
        timetables = Timetable.objects.filter(batch_id=batch_id, user=request.user)
        response_data = [
            {
                'id': t.id,
                'name': t.name,
                'year': t.year,
                'unit_code': t.unit_code,
                'unit_name': t.unit_name,
                'day': t.day,
                'start_time': t.start_time,
                'end_time': t.end_time,
                'lecturer': t.lecturer,
                'campus': t.campus,
                'mode_of_study': t.mode_of_study,
                'lecture_room': t.lecture_room,
                'group': t.group,
            } for t in timetables
        ]
        return Response(response_data, status=status.HTTP_200_OK)

# ✅ Upload units from Excel file
class UploadUnitsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, format=None):
        user = request.user
        batch_id = request.data.get('batch_id')
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        data = pd.read_excel(file)
        units = [
            Unit(user=user, unit_name=row['Unit Name'], unit_code=row['Unit Code'], year=row['Year'], batch_id=batch_id)
            for _, row in data.iterrows()
        ]
        Unit.objects.bulk_create(units)
        return Response(status=status.HTTP_201_CREATED)

# ✅ Generate timetable based on genetic algorithm (and optionally correct it with a prompt)
class GenerateTimetableView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, format=None):
        try:
            batch_id = request.data.get('batch_id')
            start_time = request.data.get('start_time')
            end_time = request.data.get('end_time')
            duration = int(request.data.get('duration'))
            first_constrain = request.data.get('first_constrain')
            second_constrain = request.data.get('second_constrain')
            prompt = request.data.get('prompt')

            # Validate input
            if not batch_id:
                return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            units = Unit.objects.filter(batch_id=batch_id)
            if not units.exists():
                return Response({"error": "No units found for the given batch_id"}, status=status.HTTP_404_NOT_FOUND)

            # Prepare data and generate timetable
            units_list = [(u.unit_name, u.unit_code, u.year) for u in units]
            best_timetable = generate_timetable(
                units_list, population_size=50, generations=100, mutation_rate=0.01,
                start_time=start_time, end_time=end_time, duration=duration,
                first_constrain=first_constrain, second_constrain=second_constrain
            )

            response_data = [
                {
                    'unit_name': s[0][0],
                    'unit_code': s[0][1],
                    'year': s[0][2],
                    'day': s[1],
                    'start_time': s[2],
                    'end_time': s[3]
                } for s in best_timetable
            ]

            # Save timetable (raw or corrected)
            sessions = double_check_timetable(response_data, prompt) if prompt else response_data
            for session in sessions:
                Timetable.objects.create(
                    user=request.user,
                    unit_name=session['unit_name'],
                    unit_code=session['unit_code'],
                    year=session['year'],
                    day=session['day'],
                    start_time=session['start_time'],
                    end_time=session['end_time'],
                    batch_id=batch_id,
                    name=batch_id
                )
            return Response(sessions, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Export timetable and send it to the user’s email as Excel
class ExportToEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, format=None):
        batch_id = request.data.get('batch_id')
        email = request.data.get('email')
        if not batch_id or not email:
            return Response({"error": "batch_id and email are required"}, status=status.HTTP_400_BAD_REQUEST)

        timetables = Timetable.objects.filter(batch_id=batch_id, user=request.user)
        if not timetables.exists():
            return Response({"error": "No timetable found for the given batch_id"}, status=status.HTTP_404_NOT_FOUND)

        # Format data for Excel export
        data = [{
            'Year': t.year,
            'Unit Code': t.unit_code,
            'Unit Name': t.unit_name,
            'Day': t.day,
            'Start Time': datetime.strptime(t.start_time, "%H:%M:%S").strftime("%H:%M"),
            'End Time': datetime.strptime(t.end_time, "%H:%M:%S").strftime("%H:%M"),
            'Lecturer': t.lecturer,
            'Campus': t.campus,
            'Mode': t.mode_of_study,
            'Room': t.lecture_room,
            'Group': t.group,
        } for t in timetables]

        # Export and email
        df = pd.DataFrame(data)
        file_name = f'timetable_{batch_id}.xlsx'
        df.to_excel(file_name, index=False)
        email_message = EmailMessage(
            subject='Your Timetable',
            body='Please find the attached timetable.',
            from_email=settings.AWS_SES_FROM_EMAIL,
            to=[email],
        )
        email_message.attach_file(file_name)
        email_message.send()
        os.remove(file_name)

        return Response({"message": "Timetable sent successfully to the provided email"}, status=status.HTTP_200_OK)
