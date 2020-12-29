from django.contrib.auth import get_user_model
from rest_framework import viewsets

from reservations.models import MeetingRoom, Reservation
from reservations.serializers import (
    EmployeeSerializer,
    MeetingRoomSerializer,
    ReservationSerializer
)

Employee = get_user_model()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
