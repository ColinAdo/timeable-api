from django.urls import path

from .views import UploadUnitsView, GenerateTimetableView, ExportTimetableView

urlpatterns = [
    path('upload_units/', UploadUnitsView.as_view(), name='upload_units'),
    path('generate_timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export_timetable/', ExportTimetableView.as_view(), name='export_timetable'),
]
