import datetime

from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=CASCADE)
    def __str__(self):
        return self.event_name
