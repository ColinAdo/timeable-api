from django.urls import path

from .views import (
    TimetableView,
    UploadUnitsView, 
    ExportToEmailView,
    GenerateTimetableView, 
    TimetableNameView,
)

urlpatterns = [
    path('upload/units/', UploadUnitsView.as_view(), name='upload_units'),
    path('timetable/names/', TimetableNameView.as_view(), name='timetable_name'),
    path('generate/timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export/timetable/', ExportToEmailView.as_view(), name='export_timetable_email'),
    path('timetable/<str:batch_id>/', TimetableView.as_view(), name='timetable'),
]
