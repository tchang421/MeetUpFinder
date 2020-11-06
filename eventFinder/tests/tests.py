from datetime import time, timedelta
from django.utils import timezone
from eventFinder.models import Event
from django.contrib.auth import models
from django.test import TestCase
from ..models import Event
from django.contrib.auth.models import User
from django.urls import *
from .test_utils import *


class DummyTest(TestCase):
    def test(self):
        self.assertTrue(True)


class EventModelTest(TestCase):
    def test_event_pub_date_is_automatically_added(self):
        testUser = make_user(username='testuser', password='12345')
        testEvent = make_event(event_name="testEvent", author=testUser)
        self.assertTrue(testEvent.pub_date > (
            timezone.now()-timedelta(minutes=1)))
        self.assertTrue(testEvent.pub_date < (
            timezone.now()+timedelta(minutes=1)))


class EventIndexViewTest(TestCase):
    def test_empty_when_no_events_added(self):
        response = self.client.get(reverse('eventFinder:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Event Name')
        self.assertQuerysetEqual(response.context['events'], [])

    def test_added_events_are_displayed(self):
        testUser = make_user(username='testuser', password='12345')
        testEvent = make_event(event_name="testEvent", author=testUser)
        response = self.client.get(reverse('eventFinder:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Event Name')
        self.assertQuerysetEqual(response.context['events'],['<Event: testEvent>'])
