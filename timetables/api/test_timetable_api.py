from datetime import time

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from timetables.models import Timetable


# Timetable api test case
class TimetableApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email = 'testuser@example.com',
            password = 'testpassword'
        )

        cls.timetable = Timetable.objects.create(
            user=cls.user,
            batch_id='shjsjhssjdjksdsjkdjssjk',
            day='monday',
            unit_code='bcs100',
            unit_name='maths',
            start_time=time(8, 0),
            end_time=time(10, 0)
        )
        cls.access_token = AccessToken.for_user(cls.user)

    def test_pst_timetable(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetable-list')
        data = {
            "user": self.user.id,
            "day": "monday",
            "unit_code": "bcs100",
            "unit_name": "maths",
            "start_time": time(2, 0),
            "end_time": time(16, 0)
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Timetable.objects.count(), 2)

    def test_get_timetable(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetable-list')
        response = self.client.get(url, format='json')
        queryset = Timetable.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, self.user.id)

    def test_retrieve_timetable(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetable-detail', kwargs={'pk': self.timetable.id})
        
        response = self.client.get(url)
        obj = Timetable.objects.get(pk=self.timetable.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.timetable.day)

    def test_update_timetable(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetable-detail', kwargs={'pk': self.timetable.id})
        data = {
            "user": self.user.id,
            "day": 'Tuesday',
            "unit_code": 'bcs100',
            "unit_name": 'maths',
            "start_time": time(2, 0),
            "end_time": time(16, 0)
        }
        response = self.client.put(url, data, format='json')
        self.timetable.refresh_from_db()
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.timetable.day, 'Tuesday')

    def test_delete_timetable(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetable-detail', kwargs={'pk': self.timetable.id})
       
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Timetable.objects.count(), 0)

    def test_timetable_detail_to_download(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('detail', kwargs={'pk': self.timetable.batch_id})

        response = self.client.get(url)
        obj = Timetable.objects.get(batch_id=self.timetable.batch_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.timetable.day)


# Timetablenames api
class TimetableNameApiTestCase(APITestCase):
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
        cls.access_token = AccessToken.for_user(cls.user)

    def test_post_timetable(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetablenames-list')
        data = {
            'user': self.user.id,
            'timetable': self.timetable.id,
            'name': 'testname2'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_timetablenames(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetablenames-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, self.user.id)

    def test_retrieve_timetablename(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetablenames-detail', kwargs={'pk': self.timetablename.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.timetablename.name)

    def test_update_timetablename(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetablenames-detail',  kwargs={'pk': self.timetablename.id})
        data = {
            "user": self.user.id,
            "timetable": self.timetable.id,
            "name": 'LMR timetable'
        }
        response = self.client.put(url, data, format='json')
        self.timetablename.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.timetablename.name, 'LMR timetable')

    def test_delete_timetablename(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('timetablenames-detail', kwargs={'pk': self.timetablename.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
