from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    health_note = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
