from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="doctors"
    )
    image = models.ImageField(upload_to='doctors/')
    experience = models.IntegerField()
    available_days = models.CharField(max_length=100)
    short_bio = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            width, height = img.size
            new_size = min(width, height)

            left = (width - new_size) / 2
            top = (height - new_size) / 2
            right = (width + new_size) / 2
            bottom = (height + new_size) / 2

            img = img.crop((left, top, right, bottom))
            img = img.resize((600, 600), Image.LANCZOS)

            img.save(self.image.path)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
    )

    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default="10:00")
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_date", "-created_at"]

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"


class HealthResource(models.Model):
    CATEGORY_CHOICES = [
        ("drugs", "Drugs & Supplements"),
        ("library", "Health Library"),
        ("research", "Research"),
        ("wellbeing", "Well-Being"),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    icon = models.CharField(max_length=50, default="fa-solid fa-heart-pulse")

    class Meta:
        ordering = ["category", "title"]

    def __str__(self):
        return self.title