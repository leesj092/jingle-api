from django.db import models
from datetime import timedelta

class Tutor(models.Model):
    name = models.CharField(max_length=100)

class Availability(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField()

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)
