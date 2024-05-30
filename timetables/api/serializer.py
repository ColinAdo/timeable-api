from rest_framework import serializers

from timetables.models import Timetable, TimetableName

class TimetableSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Timetable
        fields = '__all__'

class TimetableNameSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    timetable = TimetableSerializer()

    class Meta:
        model = TimetableName
        fields = (
            'id', 
            'name',
            'user',
            'timetable',
            'created',
        )