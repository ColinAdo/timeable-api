import pandas as pd
import uuid

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# from .permissions import IsOwnerOrReadOnly
from timetables.models import Timetable, Unit
from .genetic_algoritm import generate_timetable

from datetime import time

class UploadUnitsView(APIView): 
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
    

class GenerateTimetableView(APIView):
    def post(self, request, format=None):
        batch_id = request.data.get('batch_id')
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        units = Unit.objects.filter(batch_id=batch_id)
        if not units.exists():
            return Response({"error": "No units found for the given batch_id"}, status=status.HTTP_404_NOT_FOUND)
        
        units_list = [(unit.unit_name, unit.unit_code, unit.year) for unit in units]
        best_timetable = generate_timetable(units_list, population_size=50, generations=100, mutation_rate=0.01)
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

        return Response(response_data, status=status.HTTP_200_OK)

# # Timetable viewset
# class TimetableViewset(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#     serializer_class = TimetableSerializer

#     def get_queryset(self):
#         return Timetable.objects.filter(user=self.request.user)


# # Timetable detail view
# class TimetableDetailView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#     serializer_class = TimetableSerializer

#     def get_queryset(self):
#         pk = self.kwargs.get('pk') 
#         return Timetable.objects.filter(batch_id=pk)
 
    
# # Timetable names viewset
# class TimetableNameViewset(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#     serializer_class = TimetableNameSerializer

#     def get_queryset(self):
#         return TimetableName.objects.filter(user=self.request.user)

# # Upload excel file view 
# class UnitUploadView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [FileUploadParser]

#     def post(self, request):
#         file_obj = request.data['file']

#         try:
#             # Read the Excel file using pandas
#             df = pd.read_excel(file_obj, engine='openpyxl')
#             batch_id = str(uuid.uuid4())

#             # Assuming 'unit_code' and 'unit_name' are the column names in the Excel file
#             unit_code_list = df['unit_code'].tolist()
#             unit_name_list = df['unit_name'].tolist()
#             days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

#             # Define time slots
#             time_slots = [
#                 (time(8, 0), time(11, 0)),
#                 (time(11, 0), time(13, 0)),
#                 (time(14, 0), time(16, 0)),
#             ]

#             # Iterate over units and assign them to days and time slots
#             unit_index = 0
#             day_index = 0

#             while unit_index < len(unit_code_list):
#                 for start_time, end_time in time_slots:
#                     if unit_index >= len(unit_code_list):
#                         break

#                     unit_code = unit_code_list[unit_index]
#                     unit_name = unit_name_list[unit_index]
#                     day = days[day_index]

#                     timetable_entry, created = Timetable.objects.update_or_create(
#                         user=request.user,
#                         batch_id=batch_id,
#                         unit_code=unit_code,
#                         unit_name=unit_name,
#                         day=day,
#                         defaults={
#                             'start_time': start_time,
#                             'end_time': end_time,
#                         }
#                     )

#                     unit_index += 1

#                 day_index = (day_index + 1) % len(days)

#             TimetableName.objects.create(
#                 user=request.user,
#                 timetable=timetable_entry,
#                 name=batch_id
#             )

#         except pd.errors.EmptyDataError:
#             return Response({'message': 'The uploaded file is empty.'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(status=status.HTTP_201_CREATED)
