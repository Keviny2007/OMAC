from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/register-for-slot/', views.register_for_slot, name='register_for_slot'),
    path('api/get-available-slots/', views.get_available_slots, name='get_available_slots'),
]
