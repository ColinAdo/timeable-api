from django.urls import path

from .views import (
    TimetableView,
    UploadUnitsView, 
    GenerateTimetableView, 
    SendTimetableEmailView
)

urlpatterns = [
    path('upload/units/', UploadUnitsView.as_view(), name='upload_units'),
    path('generate/timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export/timetable/email/', SendTimetableEmailView.as_view(), name='export_timetable_email'),
    path('timetable/<str:batch_id>/', TimetableView.as_view(), name='timetable'),
]
