from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from reservations.views import (EmployeeViewSet, MeetingRoomViewSet,
                                ReservationViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Room reservations API",
        default_version="v1",
        description="This API allows to managed employees, rooms and room reservations",
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "api/employees/",
        EmployeeViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="employee-list",
    ),
    path(
        "api/employees/<int:pk>/",
        EmployeeViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="employee-detail",
    ),
    path(
        "api/meeting-rooms/",
        MeetingRoomViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="meeting-room-list",
    ),
    path(
        "api/meeting-rooms/<int:pk>/",
        MeetingRoomViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="meeting-room-detail",
    ),
    path(
        "api/reservations/",
        ReservationViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="reservation-list",
    ),
    path(
        "api/reservations/<int:pk>/",
        ReservationViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="reservation-detail",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
]
