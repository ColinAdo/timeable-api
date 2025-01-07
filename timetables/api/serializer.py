from rest_framework import serializers

from rest_framework import serializers
from timetables.models import Unit, Timetable

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'


# from timetables.models import Timetable, TimetableName

# # Timetable serializer
# class TimetableSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Timetable
#         fields = '__all__'


# # Timetable names serializer
# class TimetableNameSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')

#     class Meta:
#         model = TimetableName
#         fields = (
#             'id',
#             'name',
#             'user',
#             'timetable',
#             'created_at',
#         )
