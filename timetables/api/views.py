import os
import pandas as pd

from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.db.models import Max

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from core import settings
from .permissions import IsOwnerOrReadOnly
from timetables.models import Timetable, Unit
from .genetic_algoritm import generate_timetable, double_check_timetable

# # Get timetable data
class TimetableDataView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def get(self, request, rowId, format=None):
        timetable = Timetable.objects.get(id=rowId)
        response_data = {
            'id': timetable.id,
            'name': timetable.name,
            'unit_code': timetable.unit_code,
            'unit_name': timetable.unit_name,
            'day': timetable.day,
            'start_time': timetable.start_time,
            'end_time': timetable.end_time
        }
        return Response(response_data, status=status.HTTP_200_OK)

# Generated timetable list view
class TimetableNameView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def get(self, request, format=None):
        timetables = (
            Timetable.objects
            .values('batch_id', 'name') 
            .annotate(latest_created_at=Max('created_at'))  
            .order_by('-latest_created_at') 
        )

        response_data = [{
            'batch_id': timetable['batch_id'],
            'name': timetable['name']
            } for timetable in timetables]

        return Response(response_data, status=status.HTTP_200_OK)

# Get timetable
class TimetableView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def get(self, request, batch_id, format=None):
        timetables = Timetable.objects.filter(batch_id=batch_id, user=request.user)
        response_data = [
            {
                'id': timetable.id,
                'name': timetable.name,
                'unit_code': timetable.unit_code,
                'unit_name': timetable.unit_name,
                'day': timetable.day,
                'start_time': timetable.start_time,
                'end_time': timetable.end_time
            }
            for timetable in timetables
        ]
        return Response(response_data, status=status.HTTP_200_OK)

# Upload excel file view
class UploadUnitsView(APIView): 
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def post(self, request, format=None): 
        batch_id = request.data.get('batch_id')
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file'] 
        data = pd.read_excel(file) 
        units = [] 
        for _, row in data.iterrows(): 
            unit = Unit(unit_name=row['Unit Name'], unit_code=row['Unit Code'], year=row['Year'], batch_id=batch_id) 
            units.append(unit) 
        Unit.objects.bulk_create(units) 
        return Response(status=status.HTTP_201_CREATED)
    
# Generate timetable view
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

            if not batch_id:
                return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            units = Unit.objects.filter(batch_id=batch_id)
            if not units.exists():
                return Response({"error": "No units found for the given batch_id"}, status=status.HTTP_404_NOT_FOUND)
            
            units_list = [(unit.unit_name, unit.unit_code, unit.year) for unit in units]
            best_timetable = generate_timetable(units_list, population_size=50, generations=100, mutation_rate=0.01, start_time=start_time, end_time=end_time, duration=duration, first_constrain=first_constrain, second_constrain=second_constrain)

            response_data = [
                {
                    'unit_name': session[0][0],
                    'unit_code': session[0][1],
                    'year': session[0][2],
                    'day': session[1],
                    'start_time': session[2],
                    'end_time': session[3]
                }
                for session in best_timetable
            ]

            if prompt == '':
                for session in best_timetable: 
                    Timetable.objects.create( 
                        user=request.user,
                        unit_name=session[0][0],  
                        unit_code=session[0][1],  
                        day=session[1],              
                        start_time=session[2],
                        end_time=session[3],    
                        batch_id=batch_id,
                        name=batch_id 
                    )
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                corrected_timetable = double_check_timetable(response_data, prompt)
                for session in corrected_timetable: 
                    Timetable.objects.create( 
                        user=request.user,
                        unit_name=session["unit_name"],  
                        unit_code=session["unit_code"],  
                        day=session["day"],              
                        start_time=session["start_time"],
                        end_time=session["end_time"],    
                        batch_id=batch_id,
                        name=batch_id 
                    )

                return Response(corrected_timetable, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
# Send timetable email view
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
        
        data = [
            {
                'Unit Code': timetable.unit_code,
                'Unit Name': timetable.unit_name,
                'Day': timetable.day,
                'Start Time': timetable.start_time,
                'End Time': timetable.end_time
            }
            for timetable in timetables
        ]
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Export to Excel
        file_name = f'timetable_{batch_id}.xlsx'
        df.to_excel(file_name, index=False)

        # Send email with attachment
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
