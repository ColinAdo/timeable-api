from rest_framework import viewsets, permissions

from .serializer import TimetableSerializer
from .permisssions import IsOwnerOrReadOnly
from timetables.models import Timetable


class TimetableViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TimetableSerializer

    def get_queryset(self):
        return Timetable.objects.filter(user=self.request.user)
