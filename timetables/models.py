from django.conf import settings
from django.db import models


class Timetable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    day = models.CharField(max_length=10)
    unit_code = models.CharField(max_length=10, null=True)
    unit_name = models.CharField(max_length=200, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    lecturer = models.CharField(max_length=200, null=True, blank=True)
    campus = models.CharField(max_length=200, null=True, blank=True)
    mode_of_study = models.CharField(max_length=200, null=True, blank=True)
    lecture_room = models.CharField(max_length=200, null=True, blank=True)
    group = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('day',)

    def __str__(self):
        return f'{self.user.username} timetable'
