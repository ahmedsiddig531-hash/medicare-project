from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book'),
    path('resources/<str:category>/', views.resource_list, name='resource_list'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('my-appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('health-library/', views.health_library, name='health_library'),
    path('drugs/', views.drugs, name='drugs'),
        path('research/', views.research, name='research'),

]
