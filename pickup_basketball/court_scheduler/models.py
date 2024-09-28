from django.db import models

class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    court_number = models.IntegerField()

    def __str__(self):
        return f"Court {self.court_number}: {self.start_time} - {self.end_time}"

class Attendance(models.Model):
    name = models.CharField(max_length=100)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} attending {self.time_slot}"

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    courts = models.CharField(max_length=255)

    def __str__(self):
        return self.name
