from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

Employee = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'tesetpassword',
        }
        self.user = Employee.objects.create_user(**self.credentials)

    def test_login(self):
        # WHEN
        url = reverse('login')
        resp = self.client.post(url, data=self.credentials, follow=True)

        # THEN
        self.assertNotIn(b'errorlist', resp.content)
        self.assertTrue(resp.context['user'].is_authenticated)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(url)
        self.assertTrue(resp.context['user'].is_authenticated)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_logout(self):
        # HAVING
        resp = self.client.post(reverse('login'), data=self.credentials, follow=True)
        self.assertTrue(resp.context['user'].is_authenticated)

        # WHEN
        resp = self.client.post(reverse('logout'), follow=True)

        # THEN
        self.assertFalse(resp.context['user'].is_authenticated)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
