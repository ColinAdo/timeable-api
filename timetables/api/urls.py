from django.urls import path

from .views import (
    TimetableView,
    UploadUnitsView, 
    ExportToEmailView,
    GenerateTimetableView, 
    TimetableDataView,
    TimetableNameView,
)

urlpatterns = [
    path('upload/units/', UploadUnitsView.as_view(), name='upload_units'),
    path('timetable/names/', TimetableNameView.as_view(), name='timetable_name'),
    path('generate/timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export/timetable/', ExportToEmailView.as_view(), name='export_timetable_email'),
    path('timetable/get/<str:rowId>/', TimetableDataView.as_view(), name='timetable_data'),
    path('timetable/<str:batch_id>/', TimetableView.as_view(), name='timetable'),
]
