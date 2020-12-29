from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reservations.models import MeetingRoom

Employee = get_user_model()


class MeetingRoomsAPITests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(Employee.objects.create_user('Tom'))

        self.room_data = {
            'number': '300',
            'title': 'Security War Zone',
            'capacity': 14,
        }
        self.room = MeetingRoom.objects.create(**self.room_data)

        self.another_room_data = {
            'number': '301',
            'title': 'Standup Place',
            'capacity': 6,
        }

    def test_get_employee_list(self, *args):
        url = reverse('meeting-room-list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_json = resp.json()
        self.assertIn(self.room_data, resp_json)

    def test_create_employee(self):
        url = reverse('meeting-room-list')
        resp = self.client.post(url, data=self.another_room_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_employee_detail(self):
        url = reverse('meeting-room-detail', kwargs={'pk': self.room.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.room_data, resp.json())

    def test_update_employee(self):
        url = reverse('meeting-room-detail', kwargs={'pk': self.room.pk})
        resp = self.client.patch(url, data=self.another_room_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.another_room_data, resp.json())

    def test_delete_employee(self):
        url = reverse('meeting-room-detail', kwargs={'pk': self.room.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MeetingRoom.objects.filter(pk=self.room.pk).exists())
