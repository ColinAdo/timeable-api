from django.urls import path

from .views import (
    UnitsView,
    TimetableView,
    UploadUnitsView, 
    ExportToEmailView,
    TimetableDataView,
    TimetableNameView,
    SubscribeView,
    SubscriptionView,
    mpesa_callback,
    GenerateTimetableView, 
)

urlpatterns = [
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('user/units/', UnitsView.as_view(), name='units'),
    path('user/subscription/', SubscriptionView.as_view(), name='subscription'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('upload/units/', UploadUnitsView.as_view(), name='upload_units'),
    path('timetable/names/', TimetableNameView.as_view(), name='timetable_name'),
    path('generate/timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export/timetable/', ExportToEmailView.as_view(), name='export_timetable_email'),
    path('timetable/get/<str:rowId>/', TimetableDataView.as_view(), name='timetable_data'),
    path('timetable/<str:batch_id>/', TimetableView.as_view(), name='timetable'),
]
