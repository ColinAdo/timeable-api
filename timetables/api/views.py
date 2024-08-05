import pandas as pd
import uuid

from rest_framework import status, permissions, viewsets, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import TimetableSerializer, TimetableNameSerializer
from .permisssions import IsOwnerOrReadOnly
from timetables.models import Timetable, TimetableName

from datetime import time


# Timetable viewset
class TimetableViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TimetableSerializer

    def get_queryset(self):
        return Timetable.objects.filter(user=self.request.user)


# Timetable detail view
class TimetableDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TimetableSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk') 
        return Timetable.objects.filter(batch_id=pk)
 
    
# Timetable names viewset
class TimetableNameViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TimetableNameSerializer

    def get_queryset(self):
        return TimetableName.objects.filter(user=self.request.user)

# Upload excel file view 
class UnitUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        file_obj = request.data['file']

        try:
            # Read the Excel file using pandas
            df = pd.read_excel(file_obj, engine='openpyxl')
            batch_id = str(uuid.uuid4())

            # Assuming 'unit_code' and 'unit_name' are the column names in the Excel file
            unit_code_list = df['unit_code'].tolist()
            unit_name_list = df['unit_name'].tolist()
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

            # Define time slots
            time_slots = [
                (time(8, 0), time(11, 0)),
                (time(11, 0), time(13, 0)),
                (time(14, 0), time(16, 0)),
            ]

            # Iterate over units and assign them to days and time slots
            unit_index = 0
            day_index = 0

            while unit_index < len(unit_code_list):
                for start_time, end_time in time_slots:
                    if unit_index >= len(unit_code_list):
                        break

                    unit_code = unit_code_list[unit_index]
                    unit_name = unit_name_list[unit_index]
                    day = days[day_index]

                    timetable_entry, created = Timetable.objects.update_or_create(
                        user=request.user,
                        batch_id=batch_id,
                        unit_code=unit_code,
                        unit_name=unit_name,
                        day=day,
                        defaults={
                            'start_time': start_time,
                            'end_time': end_time,
                        }
                    )

                    unit_index += 1

                day_index = (day_index + 1) % len(days)

            TimetableName.objects.create(
                user=request.user,
                timetable=timetable_entry,
                name=batch_id
            )

        except pd.errors.EmptyDataError:
            return Response({'message': 'The uploaded file is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)
