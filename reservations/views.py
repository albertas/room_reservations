import logging

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

logger = logging.getLogger(__name__)

Employee = get_user_model()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET employee-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST employee-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET employee {pk} with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} PATCH employee {pk} with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().partial_update(request, pk, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        logger.info(f"User {request.user} DELETE employee {pk}")
        return super().destroy(request, pk, *args, **kwargs)


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET meeting-room-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST meeting-room-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET meeting-room {pk} with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} PATCH meeting-room {pk} with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().partial_update(request, pk, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        logger.info(f"User {request.user} DELETE meeting-room {pk}")
        return super().destroy(request, pk, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ReservationFilter

    def list(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} GET reservation-list with args {dict(request.query_params)}"
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(
            f"User {request.user} POST reservation-list with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} GET reservation {pk} with args {dict(request.query_params)}"
        )
        return super().retrieve(request, pk, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        logger.info(
            f"User {request.user} PATCH reservation {pk} with args "
            f"{dict(request.query_params)} and data {request.data}"
        )
        return super().partial_update(request, pk, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        logger.info(f"User {request.user} DELETE reservation {pk}")
        return super().destroy(request, pk, *args, **kwargs)


def index(request):
    return HttpResponseRedirect(reverse("swagger-ui"))
