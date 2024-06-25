from django.contrib import admin

from .models import Timetable, TimetableName

# Timetable admin
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


class TimetableNameAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "timetable",
        "name",
        "created_at",
    ]


admin.site.register(Timetable, TimetableAdmin)
admin.site.register(TimetableName, TimetableNameAdmin)
