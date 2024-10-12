from django.urls import path
from . import views
from court_scheduler.views import weekly_calendar_view

urlpatterns = [
    path('', weekly_calendar_view, name='weekly_calendar'),
    path('api/register-for-slot/', views.register_for_slot, name='register_for_slot'),
    path('api/get-available-slots/', views.get_available_slots, name='get_available_slots'),
]
