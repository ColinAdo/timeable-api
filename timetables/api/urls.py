from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    TimetableViewset, 
    UnitUploadView, 
    TimetableNameViewset, 
    TimetableDetailView
)

router = DefaultRouter()

urlpatterns = [
    path('upload/', UnitUploadView.as_view(), name='upload'),
    path('timetabledetail/<str:pk>/', TimetableDetailView.as_view(), name='detail'),
]

router.register(r'timetable', TimetableViewset, basename='timetable')
router.register(r'timetablenames', TimetableNameViewset, basename='timetablenames')
urlpatterns += router.urls
