from django.shortcuts import render
from django.http import JsonResponse
from .models import TimeSlot, Attendance
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from court_scheduler.models import Event
from court_scheduler.weekly_calendar_view_logic import generate_time_range, calculate_free_slots
import pprint

def login_view(request):
    return render(request, 'court_scheduler/login.html')

def calendar_view(request):
    return render(request, 'court_scheduler/calendar.html')

@csrf_exempt
def register_for_slot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        slot_id = data.get('slot_id')
        time_slot = TimeSlot.objects.get(id=slot_id)
        Attendance.objects.create(name=name, time_slot=time_slot)
        return JsonResponse({'status': 'success'})

def get_available_slots(request):
    slots = TimeSlot.objects.all().values('id', 'start_time', 'end_time', 'court_number')
    return JsonResponse(list(slots), safe=False)

def weekly_calendar_view(request):
    print('hi')

    # YYYY-MM-DD
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday() + 1)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    events = Event.objects.filter(start_time__date__range=(start_of_week, end_of_week))

    week_dates = sorted(set(event.start_time.date() for event in events))  # Get unique dates

    # OMAC hours (6:00:00 - 23:00:00)
    omac_open_time = datetime.time(6, 0)
    omac_close_time = datetime.time(23, 0)

    # For each day, calculate the free slots by subtracting event times
    free_slots_by_day = {}
    for date in week_dates:
        # Get all events for the current date
        day_events = events.filter(start_time__date=date)
        free_slots = calculate_free_slots(day_events, omac_open_time, omac_close_time)
        free_slots_by_day[date] = free_slots
    # pprint.pprint(free_slots_by_day)
    context = {
        'week_dates': week_dates,  # Pass the list of dates
        'free_slots_by_day': free_slots_by_day, # Free slots for each day
        'today': today,
    }
    
    return render(request, 'court_scheduler/calendar.html', context)

def test_view(request):
    context = {'test': 'hello world'}
    print('hi')
    return render(request, 'court_scheduler/test.html', context)

