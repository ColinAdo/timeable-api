from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Timetable, TimetableName

from datetime import time


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
        self.assertEqual(obj.user.username, self.user.username)
        self.assertEqual(obj.day, self.timetable.day)
        self.assertEqual(obj.unit_code, self.timetable.unit_code)
        self.assertEqual(obj.unit_name, self.timetable.unit_name)
        self.assertEqual(obj.start_time, self.timetable.start_time)
        self.assertEqual(obj.end_time, self.timetable.end_time)
        self.assertEqual(str(self.timetable), f'{self.user.username} timetable')


# Timetablename test case class
class TestTimetableName(TestCase):
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
        cls.timetablename = TimetableName.objects.create(
            user=cls.user,
            timetable=cls.timetable,
            name='testname'
        )

    def test_timetablename_content(self):
        obj = TimetableName.objects.get(id=1)
        self.assertEqual(Timetable.objects.count(), 1)
        self.assertEqual(obj.user.username, self.user.username)
        self.assertEqual(obj.timetable, self.timetable)
        self.assertEqual(str(obj.name), f'{self.timetablename.name}')