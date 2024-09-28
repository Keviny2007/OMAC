from django.contrib import admin
from .models import Event

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'courts')  # Adjust these fields based on your model
    search_fields = ('name',)  # Enables search for the event name