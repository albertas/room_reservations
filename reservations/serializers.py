from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from reservations.models import MeetingRoom, Reservation

Employee = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["username", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        employee = Employee.objects.create(**validated_data)
        if password:
            employee.set_password(validated_data["password"])
            employee.save()
        return employee


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        exclude = ["reservations"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("canceled") is False:
            representation.pop("canceled")
        return representation

    def validate(self, data):
        if "booked_from" in data or "booked_till" in data or "room" in data:
            booked_from = data.get("booked_from") or self.instance.booked_from
            booked_till = data.get("booked_till") or self.instance.booked_till
            room = data.get("room") or self.instance.room

            contains = Q(
                booked_from__lte=booked_from,
                booked_till__gte=booked_till,
                room=room,
                canceled=False,
            )
            overlaps_at_start = Q(
                booked_till__gt=booked_from,
                booked_till__lt=booked_till,
                room=room,
                canceled=False,
            )
            overlaps_at_end = Q(
                booked_from__gt=booked_from,
                booked_from__lt=booked_till,
                room=room,
                canceled=False,
            )
            overlaps = contains | overlaps_at_start | overlaps_at_end
            if Reservation.objects.filter(overlaps).exists():
                message = f"Requested time overlaps with another reservation in room {room.pk}"
                raise serializers.ValidationError(message)
        return data
