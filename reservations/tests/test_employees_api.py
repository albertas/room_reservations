from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


Employee = get_user_model()


class SwaggerPageTests(APITestCase):
    def setUp(self):
        self.employee_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'test',
            'last_name': 'user',
        }
        self.employee = Employee.objects.create_user(
            password='test',
            **self.employee_data
        )
        self.client.force_authenticate(self.employee)

        self.new_employee_data = {
            'username': 'anotheruser',
            'email': 'another@example.com',
            'first_name': 'another',
            'last_name': 'user'
        }

    def test_get_employee_list(self, *args):
        Employee.objects.create_user(password='test', **self.new_employee_data)

        url = reverse('employee-list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(self.new_employee_data, resp.json())

    def test_create_employee(self):
        url = reverse('employee-list')
        resp = self.client.post(url, data=self.new_employee_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_employee_detail(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.employee_data, resp.json())

    def test_update_employee(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        resp = self.client.patch(url, data=self.new_employee_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.new_employee_data, resp.json())

    def test_delete_employee(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
