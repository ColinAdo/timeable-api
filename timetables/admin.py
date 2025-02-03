from django.contrib import admin

from .models import Timetable, Unit, Subscription

# Unit admin
class UnitAdmin(admin.ModelAdmin):
    list_display = [
        'batch_id',
        'unit_code',
        'unit_name',
        'year',
    ]

# Timetable admin
class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        # 'user',
        'name',
        'unit_code',
        'unit_name',
        'day',
        'start_time',
        'end_time',
        # 'lecturer',
        # 'campus',
        # 'mode_of_study',
        # 'lecture_room',
        # 'group',
    ]

# Subscription admin
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'status',
        'tier',
        'amount',
    ]

admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Subscription, SubscriptionAdmin)