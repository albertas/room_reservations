from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SwaggerPageTests(APITestCase):
    def test_swagger_page(self):
        url = reverse("swagger-ui")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
