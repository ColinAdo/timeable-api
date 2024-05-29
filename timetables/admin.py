from django.contrib import admin

from .models import Timetable


class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "unit",
        "day",
        "start_time",
        "end_time",
        "created_at"
    ]


admin.site.register(Timetable, TimetableAdmin)
