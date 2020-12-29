from django.contrib.auth import get_user_model
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
