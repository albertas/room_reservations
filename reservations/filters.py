from django_filters import rest_framework as filters

from reservations.models import Reservation


class ReservationFilter(filters.FilterSet):
    booked_from__lte = filters.DateTimeFilter(field_name="booked_from", lookup_expr="lte")
    booked_from__gte = filters.DateTimeFilter(field_name="booked_from", lookup_expr="gte")
    booked_till__lte = filters.DateTimeFilter(field_name="booked_till", lookup_expr="lte")
    booked_till__gte = filters.DateTimeFilter(field_name="booked_till", lookup_expr="gte")
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

    def attendees_filter(self, queryset, name, value):
        for attendee_pk in value.split(","):
            queryset = queryset.filter(attendees=attendee_pk.strip())
        return queryset
