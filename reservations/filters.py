from django.urls import reverse
from django_filters import rest_framework as filters

from reservations.models import Reservation


class ReservationFilter(filters.FilterSet):
    booked_from__lte = filters.DateTimeFilter(field_name="booked_from", lookup_expr="lte")
    booked_from__gte = filters.DateTimeFilter(field_name="booked_from", lookup_expr="gte")
    booked_till__lte = filters.DateTimeFilter(field_name="booked_till", lookup_expr="lte")
    booked_till__gte = filters.DateTimeFilter(field_name="booked_till", lookup_expr="gte")
    include_canceled = filters.BooleanFilter(
        method="include_canceled_filter",
        help_text='Canceled reservations are excluded by default, use "true" to include them.',
    )
    attendees = filters.CharFilter(
        method="attendees_filter",
        help_text=(
            "Filter by one or more attendees separated by comma, e.g. tom,bob. "
            "Reservations where all attendees are participating in will be found."
        ),
    )

    class Meta:
        model = Reservation
        fields = [
            "attendees",
            "room",
            "booked_by",
            "booked_from",
            "booked_till",
            "booked_from__lte",
            "booked_from__gte",
            "booked_till__lte",
            "booked_till__gte",
        ]

    def __init__(self, data=None, *args, **kwargs):
        is_list_url = kwargs.get("request") is not None and kwargs.get("request").path == reverse(
            "reservation-list"
        )
        if is_list_url and data is not None and "include_canceled" not in data:
            data = data.copy()
            data["include_canceled"] = "false"
        super().__init__(data, *args, **kwargs)

    def attendees_filter(self, queryset, name, value):
        for attendee_pk in value.split(","):
            queryset = queryset.filter(attendees=attendee_pk.strip())
        return queryset

    def include_canceled_filter(self, queryset, name, value):
        if value is False:
            queryset = queryset.filter(canceled=False)
        return queryset
