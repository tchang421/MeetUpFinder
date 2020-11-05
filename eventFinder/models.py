import datetime

from django.db import models
from django.db.models.deletion import CASCADE
from django.urls.base import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    event_description = models.CharField(max_length=1000, default="Generic Event Description")
    author = models.ForeignKey(User, null=True, on_delete=CASCADE)

    def __str__(self):
        return self.event_name
    
    def get_absolute_url(self):
        return reverse("eventFinder:show", kwargs={"pk": self.pk})
    
