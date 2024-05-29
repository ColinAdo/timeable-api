from datetime import timedelta

from .models import Timetable


def generate_timetable(unit, user):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    start_time = timedelta(hours=8)
    end_time = timedelta(hours=11)

    for day in days:
        if not Timetable.objects.filter(day=day, start_time__lte=start_time, end_time__gte=end_time).exists():
            Timetable.objects.create(
                user=user,  # Set the user field
                unit=unit,
                day=day,
                start_time=start_time.total_seconds() // 3600,
                end_time=end_time.total_seconds() // 3600
            )
            start_time += timedelta(hours=3)
            end_time += timedelta(hours=3)
        else:
            continue
