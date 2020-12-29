from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from reservations.models import MeetingRoom, Reservation


Employee = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        employee = Employee.objects.create(**validated_data)
        if password:
            employee.set_password(validated_data['password'])
            employee.save()
        return employee


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        exclude = ['reservations']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        contains = Q(
            booked_from__lte=data['booked_from'],
            booked_till__gte=data['booked_till'],
            room=data['room']
        )
        overlaps_at_start = Q(
            booked_till__gt=data['booked_from'],
            booked_till__lt=data['booked_till'],
            room=data['room']
        )
        overlaps_at_end = Q(
            booked_from__gt=data['booked_from'],
            booked_from__lt=data['booked_till'],
            room=data['room']
        )
        overlaps = contains | overlaps_at_start | overlaps_at_end
        if Reservation.objects.filter(overlaps).exists():
            message = "Requested time overlaps with another reservation in that room"
            raise serializers.ValidationError(message)
        return data
