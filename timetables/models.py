from django.db import models
from django.conf import settings

# Unit model
class Unit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    batch_id = models.CharField(max_length=50, blank=True, null=True)
    unit_name = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=10)
    year = models.CharField(max_length=10)

# timetable model
class Timetable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    batch_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_code = models.CharField(max_length=10, blank=True, null=True)
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    day = models.CharField(max_length=10, blank=True, null=True)
    start_time = models.CharField(max_length=10, blank=True, null=True)
    end_time = models.CharField(max_length=10, blank=True, null=True)
    lecturer = models.CharField(max_length=200, null=True, blank=True)
    campus = models.CharField(max_length=200, null=True, blank=True)
    mode_of_study = models.CharField(max_length=200, null=True, blank=True)
    lecture_room = models.CharField(max_length=200, null=True, blank=True)
    group = models.CharField(max_length=200, default=0, null=True, blank=True)
    year = models.CharField(max_length=200, default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} timetable'

# Subscription model
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=99999999, decimal_places=2)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    tier = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Subscriptions'
    
class PendingTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)