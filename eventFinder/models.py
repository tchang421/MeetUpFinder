import datetime

from django.db import models
from django.db.models.deletion import CASCADE
from django.urls.base import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# from userprofile.models import UserProfile
from address.models import AddressField
from geopy.geocoders.googlev3 import GoogleV3


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    event_description = models.CharField(
        max_length=1000, default="No Description Provided")
    author = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='events_created')
    address = AddressField(null=True)
    latitude = models.DecimalField(
        decimal_places=7, max_digits=10, default=38.0336)
    longitude = models.DecimalField(
        decimal_places=7, max_digits=10, default=-78.507980)
    attendees = models.ManyToManyField(User, related_name="events_attended")

    def save(self, *args, **kwargs):

        # save coordinates by geocoding address
        geolocator = GoogleV3(
            api_key='AIzaSyDwMQvVq5I887bnz3zAlz71Onjsq4_PYb0')
        location = None if not self.address else geolocator.geocode(
            self.address)
        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude

        super().save(*args, **kwargs)

        # save author to attendees
        self.attendees.add(self.author)

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse("eventFinder:show", kwargs={"pk": self.pk})

    def add_attendee(self, attendee, *args, **kwargs):
        self.attendees.add(attendee)
    def remove_attendee(self, attendee, *args, **kwargs):
        self.attendees.remove(attendee)