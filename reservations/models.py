from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    def __str__(self):
        return self.username
