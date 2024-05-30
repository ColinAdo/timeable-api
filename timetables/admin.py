from django.contrib import admin

from .models import Timetable


class TimetableAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "unit_code",
        "unit_name",
        "day",
        "start_time",
        "end_time",
        "lecturer",
        "campus",
        "mode_of_study",
        "lecture_room",
        "group",
    ]


admin.site.register(Timetable, TimetableAdmin)
