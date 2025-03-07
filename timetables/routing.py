from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('api/v1/timetable/', consumers.TimetableConsumer.as_asgi()),
]