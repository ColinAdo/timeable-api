from django.db import models
from django.conf import settings

# Unit model
class Unit(models.Model):
    batch_id = models.CharField(max_length=50, blank=True, null=True)
    unit_name = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=10)
    year = models.CharField(max_length=10)

# timetable model
class Timetable(models.Model):
    batch_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_code = models.CharField(max_length=10, blank=True, null=True)
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    day = models.CharField(max_length=10)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     lecturer = models.CharField(max_length=200, null=True, blank=True)
#     campus = models.CharField(max_length=200, null=True, blank=True)
#     mode_of_study = models.CharField(max_length=200, null=True, blank=True)
#     lecture_room = models.CharField(max_length=200, null=True, blank=True)
#     group = models.IntegerField(default=0, null=True, blank=True)

#     class Meta:
#         ordering = ('day',)

#     def __str__(self):
#         return f'{self.user.username} timetable'

# Subscription model
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=99999999, decimal_places=2)
    tier = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Subscriptions'