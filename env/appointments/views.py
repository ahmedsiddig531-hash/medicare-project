from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm
from .models import Appointment, Department, Doctor, HealthResource


def home(request):
    doctors = Doctor.objects.all()[:3]
    departments = Department.objects.all()[:4]
    resources = HealthResource.objects.all()[:4]
    return render(
        request,
        "appointments/home.html",
        {
            "doctors": doctors,
            "departments": departments,
            "resources": resources,
        },
    )


def doctors(request):
    return render(
        request,
        "appointments/doctors.html",
        {"doctors": Doctor.objects.select_related("department").all()},
    )


def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    initial = {}
    if request.user.is_authenticated:
        initial = {
            "patient_name": request.user.get_full_name() or request.user.username,
            "patient_email": request.user.email,
        }

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            if request.user.is_authenticated:
                appointment.user = request.user
            appointment.save()
            messages.success(
                request,
                "Your appointment request was submitted successfully.",
            )
            return redirect("book", doctor_id=doctor.id)
    else:
        form = AppointmentForm(initial=initial)

    return render(
        request,
        "appointments/book.html",
        {"doctor": doctor, "form": form},
    )


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor.objects.select_related("department"), id=doctor_id)
    related_resources = HealthResource.objects.all()[:3]
    return render(
        request,
        "appointments/doctor_detail.html",
        {"doctor": doctor, "related_resources": related_resources},
    )


def resource_list(request, category):
    category_titles = {
        "drugs": "Drugs & Supplements",
        "library": "Health Library",
        "research": "Research",
        "wellbeing": "Well-Being",
    }
    resources = HealthResource.objects.filter(category=category)
    return render(
        request,
        "appointments/resource_list.html",
        {
            "resources": resources,
            "page_title": category_titles.get(category, "Resources"),
            "category": category,
        },
    )


def search(request):
    query = request.GET.get("q", "").strip()
    doctors = Doctor.objects.none()
    departments = Department.objects.none()
    resources = HealthResource.objects.none()

    if query:
        doctors = Doctor.objects.filter(
            Q(name__icontains=query)
            | Q(specialty__icontains=query)
            | Q(short_bio__icontains=query)
        )
        departments = Department.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        resources = HealthResource.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )

    return render(
        request,
        "appointments/search.html",
        {
            "query": query,
            "doctors": doctors,
            "departments": departments,
            "resources": resources,
        },
    )


@login_required
def my_appointments(request):
    appointments = Appointment.objects.select_related("doctor").filter(
        user=request.user
    )
    return render(
        request,
        "appointments/my_appointments.html",
        {"appointments": appointments},
    )


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user,
    )
    if request.method == "POST" and appointment.status == "pending":
        appointment.status = "cancelled"
        appointment.save(update_fields=["status"])
        messages.success(request, "Your appointment has been cancelled.")
    return redirect("my_appointments")
def wellbeing(request):
    return render(request, 'appointments/wellbeing.html')
def health_library(request):
    return render(request, 'appointments/health_library.html')
def drugs(request):
    return render(request, 'appointments/drugs.html')
def research(request):
    return render(request, 'appointments/research.html')