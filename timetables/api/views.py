import pandas as pd
import uuid

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
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
