from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TimetableViewset, UnitUploadView, TimetableNameView, TimetableDetailView

router = DefaultRouter()


urlpatterns = [
    path('upload/', UnitUploadView.as_view(), name='upload'),
    path('name/', TimetableNameView.as_view(), name='name'),
    path('timetabledetail/<str:pk>/', TimetableDetailView.as_view(), name='detail'),
]

router.register(r'timetable', TimetableViewset, basename='timetable')
urlpatterns += router.urls
