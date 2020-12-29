from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework import viewsets

from reservations.filters import ReservationFilter
from reservations.models import MeetingRoom, Reservation
from reservations.serializers import (EmployeeSerializer,
                                      MeetingRoomSerializer,
                                      ReservationSerializer)

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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ReservationFilter


def index(request):
    return HttpResponseRedirect(reverse("swagger-ui"))
