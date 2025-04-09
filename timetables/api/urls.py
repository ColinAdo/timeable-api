from django.urls import path

from .views import (
    UnitsView,
    TimetableView,
    SubscribeView,
    mpesa_callback,
    UploadUnitsView, 
    SubscriptionView,
    ExportToEmailView,
    TimetableDataView,
    TimetableNameView,
    GenerateTimetableView, 
)

urlpatterns = [
    path('user/units/', UnitsView.as_view(), name='units'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('upload/units/', UploadUnitsView.as_view(), name='upload_units'),
    path('user/subscription/', SubscriptionView.as_view(), name='subscription'),
    path('timetable/names/', TimetableNameView.as_view(), name='timetable_name'),
    path('timetable/<str:batch_id>/', TimetableView.as_view(), name='timetable'),
    path('generate/timetable/', GenerateTimetableView.as_view(), name='generate_timetable'),
    path('export/timetable/', ExportToEmailView.as_view(), name='export_timetable_email'),
    path('timetable/get/<str:rowId>/', TimetableDataView.as_view(), name='timetable_data'),
]
