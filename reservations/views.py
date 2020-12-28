from django.contrib.auth import get_user_model
from rest_framework import viewsets

from reservations.serializers import EmployeeSerializer

Employee = get_user_model()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
