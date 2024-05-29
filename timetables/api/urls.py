from rest_framework.routers import DefaultRouter

from .views import TimetableViewset

router = DefaultRouter()

router.register(r'timetable', TimetableViewset, basename='timetable')
urlpatterns = router.urls
