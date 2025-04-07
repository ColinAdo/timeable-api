from rest_framework import serializers

from rest_framework import serializers
from timetables.models import Unit, Timetable

# Units serializer
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'