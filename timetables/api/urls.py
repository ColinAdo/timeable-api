from django.urls import path

from .views import (
    UploadUnitsView, 
    GenerateTimetableView, 
    ExportTimetableView,
    SendTimetableEmailView
)

urlpatterns = [
    path('upload/units/', UploadUnitsView.as_view(), name='upload_units'),
    path('generate/timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export/timetable/', ExportTimetableView.as_view(), name='export_timetable'),
    path('export/timetable/email/', SendTimetableEmailView.as_view(), name='export_timetable_email'),
]
