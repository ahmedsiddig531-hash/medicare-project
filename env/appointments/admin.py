from django.contrib import admin
from .models import Appointment, Department, Doctor, HealthResource


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "department", "experience", "available_days")
    list_filter = ("department",)
    search_fields = ("name", "specialty")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "doctor", "appointment_date", "appointment_time", "status")
    list_filter = ("appointment_date", "doctor", "status")
    search_fields = ("patient_name", "patient_email", "phone_number")


@admin.register(HealthResource)
class HealthResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    list_filter = ("category",)
    search_fields = ("title", "summary")
