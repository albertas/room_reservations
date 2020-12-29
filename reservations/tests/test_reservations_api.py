from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from parameterized import parameterized

from reservations.models import MeetingRoom, Reservation


Employee = get_user_model()


class ReservationsAPITests(APITestCase):
    def setUp(self):
        self.employee1 = Employee.objects.create_user('Tom')
        self.employee2 = Employee.objects.create_user('Bob')
        self.employee3 = Employee.objects.create_user('John')

        self.client.force_authenticate(self.employee1)

        self.room1 = MeetingRoom.objects.create(number='300')
        self.room2 = MeetingRoom.objects.create(number='301')

        self.reservation = Reservation.objects.create(
            room=self.room1,
            booked_from='2020-01-01T10:00:00Z',
            booked_till='2020-01-01T10:30:00Z',
            booked_by=self.employee1,
            title='Weekly meeting',
        )
        self.reservation.attendees.set([
            self.employee1.pk, self.employee2.pk, self.employee3.pk
        ])

        self.new_reservation_data = {
            'room': self.room2.pk,
            'booked_from': '2020-01-01T11:00:00Z',
            'booked_till': '2020-01-01T11:30:00Z',
            'booked_by': self.employee1.pk,
            'title': 'Weekly meeting',
            'attendees': [self.employee1.pk, self.employee2.pk, self.employee3.pk]
        }

    def test_get_reservation_list(self, *args):
        url = reverse('reservation-list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.json()[0]['room'], self.room1.pk)
        self.assertEqual(resp.json()[0]['booked_from'], '2020-01-01T10:00:00Z')
        self.assertEqual(resp.json()[0]['booked_till'], '2020-01-01T10:30:00Z')
        self.assertEqual(resp.json()[0]['booked_by'], self.employee1.pk)
        self.assertEqual(resp.json()[0]['title'], 'Weekly meeting')
        self.assertEqual(resp.json()[0]['attendees'], [
            self.employee1.pk, self.employee2.pk, self.employee3.pk
        ])

    def test_create_reservation(self):
        url = reverse('reservation-list')
        resp = self.client.post(url, data=self.new_reservation_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp_data = resp.json()
        resp_data.pop('id')
        self.assertEqual(resp_data, self.new_reservation_data)

    def test_get_reservation_detail(self):
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['room'], self.room1.pk)
        self.assertEqual(resp.json()['booked_from'], '2020-01-01T10:00:00Z')
        self.assertEqual(resp.json()['booked_till'], '2020-01-01T10:30:00Z')
        self.assertEqual(resp.json()['booked_by'], self.employee1.pk)
        self.assertEqual(resp.json()['title'], 'Weekly meeting')
        self.assertEqual(resp.json()['attendees'], [
            self.employee1.pk, self.employee2.pk, self.employee3.pk
        ])

    def test_update_reservation(self):
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        resp = self.client.patch(url, data=self.new_reservation_data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_data = resp.json()
        resp_data.pop('id')
        self.assertEqual(self.new_reservation_data, resp_data)

    def test_delete_reservation(self):
        url = reverse('reservation-detail', kwargs={'pk': self.reservation.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(pk=self.reservation.pk).exists())

    @parameterized.expand((
        # Try to book the same reservation
        ['2020-01-01T11:00:00Z', '2020-01-01T11:30:00Z', status.HTTP_400_BAD_REQUEST],

        # Try to book overlaping at the begining reservation
        ['2020-01-01T11:00:00Z', '2020-01-01T11:10:00Z', status.HTTP_400_BAD_REQUEST],

        # Try to book overlaping at the end reservation
        ['2020-01-01T11:10:00Z', '2020-01-01T11:30:00Z', status.HTTP_400_BAD_REQUEST],

        # Try to book reservation which is inside already existing reservation
        ['2020-01-01T11:10:00Z', '2020-01-01T11:20:00Z', status.HTTP_400_BAD_REQUEST],

        # Try to book reservation which contains already existing reservation
        ['2020-01-01T10:00:00Z', '2020-01-01T12:00:00Z', status.HTTP_400_BAD_REQUEST],

        # Try to book non-overlaping reservation
        ['2020-01-01T12:00:00Z', '2020-01-01T13:00:00Z', status.HTTP_201_CREATED],
    ))
    def test_create_overlapping_reservations(self, booked_from, booked_till, status_code):
        url = reverse('reservation-list')
        reservation_data = self.new_reservation_data.copy()
        reservation_data['booked_from'] = '2020-01-01T11:00:00Z',
        reservation_data['booked_till'] = '2020-01-01T11:30:00Z',
        resp = self.client.post(url, data=reservation_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Try to book another reservation for the same room
        reservation_data['booked_from'] = booked_from
        reservation_data['booked_till'] = booked_till
        resp = self.client.post(url, data=reservation_data)
        self.assertEqual(resp.status_code, status_code)
