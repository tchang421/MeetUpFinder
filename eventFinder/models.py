import datetime

from django.db import models
from django.utils import timezone

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.event_name
