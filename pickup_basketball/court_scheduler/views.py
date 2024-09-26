from django.shortcuts import render
from django.http import JsonResponse
from .models import TimeSlot, Attendance
from django.views.decorators.csrf import csrf_exempt
import json

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
