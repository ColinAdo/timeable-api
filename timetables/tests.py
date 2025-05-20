from datetime import time
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Timetable

# Timetable test case class                                                                                 
class TestTimetable(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        cls.timetable = Timetable.objects.create(
            user=cls.user,
            day='monday',
            unit_code='bcs100',
            unit_name='maths',
            start_time=time(8, 0),
            end_time=time(10, 0)
        )

    def test_timetable_content(self):
        obj = Timetable.objects.get(id=1)
        self.assertEqual(Timetable.objects.count(), 1)
        self.assertEqual(obj.user, self.user)
        self.assertEqual(obj.day, self.timetable.day)
        self.assertEqual(obj.unit_code, self.timetable.unit_code)
        self.assertEqual(obj.unit_name, self.timetable.unit_name)
        self.assertEqual(str(obj.start_time), str(self.timetable.start_time))
        self.assertEqual(str(obj.end_time), str(self.timetable.end_time))
        self.assertEqual(str(self.timetable), f'{self.user.username} timetable')
