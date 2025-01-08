from django.urls import path

from django.urls import path
from .views import UploadUnitsView, GenerateTimetableView

urlpatterns = [
    path('upload_units/', UploadUnitsView.as_view(), name='upload_units'),
    path('generate_timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
]
