from rest_framework import serializers

from timetables.models import Timetable, TimetableName

# Timetable serializer
class TimetableSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Timetable
        fields = '__all__'


# Timetable names serializer
class TimetableNameSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    timetable = TimetableSerializer(read_only=True)

    class Meta:
        model = TimetableName
        fields = (
            'id',
            'name',
            'user',
            'timetable',
            'created',
        )
