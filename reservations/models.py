from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Employee(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        primary_key=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]


class MeetingRoom(models.Model):
    number = models.CharField(max_length=32, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    reservations = models.ManyToManyField(Employee, through="Reservation")


class Reservation(models.Model):
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="reservations")
    title = models.CharField(max_length=255, null=True, blank=True)
    booked_from = models.DateTimeField()
    booked_till = models.DateTimeField()
    attendees = models.ManyToManyField(Employee, related_name="invited_to")
    canceled = models.BooleanField(default=False)
