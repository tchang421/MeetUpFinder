from datetime import time, timedelta
from django.http import response
from django.utils import timezone
from eventFinder.models import Event
from django.contrib.auth import login, models
from django.test import TestCase
from ..models import Event
from django.contrib.auth.models import User
from django.urls import *
from .test_utils import *


class DummyTest(TestCase):
    # You know, to test that we set up the tests file itself correctly
    def test(self):
        self.assertTrue(True)


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = make_user(username='testuser', password='12345')
        cls.test_event = make_event(
            event_name="testEvent", author=cls.test_user)

    def test_event_pub_date_is_automatically_added(self):
        self.assertTrue(self.test_event.pub_date > (
            timezone.now()-timedelta(minutes=1)))
        self.assertTrue(self.test_event.pub_date < (
            timezone.now()+timedelta(minutes=1)))

    def test_get_absolute_url(self):
        correctURL = reverse('eventFinder:show', kwargs={
                             'pk': self.test_event.pk})
        self.assertEqual(correctURL, self.test_event.get_absolute_url())


class EventIndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = make_user(username='testuser', password='12345')

    def test_has_create_event_button(self):
        response = self.client.get(reverse(('eventFinder:index')))
        self.assertContains(response, reverse('eventFinder:create'))

    def test_empty_when_no_events_added(self):
        response = self.client.get(reverse('eventFinder:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Event Name')
        self.assertQuerysetEqual(response.context['events'], [])

    def test_added_events_are_displayed(self):
        test_event = make_event(event_name="testEvent", author=self.test_user)
        response = self.client.get(reverse('eventFinder:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Event Name')
        self.assertContains(response, reverse(
            'eventFinder:show', kwargs={"pk": test_event.pk}))
        self.assertQuerysetEqual(response.context['events'], [
                                 '<Event: testEvent>'])


class EventShowViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = make_user(username='testuser', password='12345')
        cls.wrong_user = make_user(username='wronguser', password='12345')
        cls.test_event = make_event(
            event_name="testEvent", author=cls.test_user)

    def test_page_has_link_to_profile(self):
        response = self.client.get(
            reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse(
            'userprofile:show', kwargs={'pk': self.test_user.profile.pk}))

    def test_no_update_or_delete_links_when_not_logged_in(self):
        response = self.client.get(
            reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse(
            'eventFinder:update', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse(
            'eventFinder:delete', kwargs={"pk": self.test_event.pk}))

    def test_no_update_or_delete_links_with_wrong_user(self):
        self.client.login(username='wronguser', password='12345')
        response = self.client.get(
            reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse(
            'eventFinder:update', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse(
            'eventFinder:delete', kwargs={"pk": self.test_event.pk}))

    def test_has_update_and_delete_links_with_correct_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse(
            'eventFinder:update', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse(
            'eventFinder:delete', kwargs={"pk": self.test_event.pk}))


class EventCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = make_user(username='testuser', password='12345')

    def login_and_create_event(self):
        self.client.login(username='testuser', password='12345')
        return self.client.post(reverse('eventFinder:create'), {
            'event_name': 'test event logged in',
            'event_type': 'Academic',
            'event_description': 'testevent',
            'event_time': '11/23/2020 23:32',
            'address': 'University of Virginia'
        })

    def test_redirect_when_get_without_login(self):
        response = self.client.get(reverse('eventFinder:create'))
        self.assertRedirects(response, reverse(
            'login')+"?next=/events/create/")

    def test_redirect_when_get_without_login(self):
        response = self.client.post(reverse('eventFinder:create'), {
            'event_name': 'test event no login',
        })
        self.assertRedirects(response, reverse(
            'login')+"?next=/events/create/")
        self.assertFalse(Event.objects.filter(
            event_name='test event no login').exists())

    def test_can_create_when_logged_in(self):
        self.login_and_create_event()
        self.assertTrue(Event.objects.filter(
            event_name='test event logged in').exists())

        new_event = Event.objects.filter(event_name='test event logged in')[0]
        self.assertEqual(new_event.author, self.test_user)

    def test_author_auto_added(self):
        self.login_and_create_event()
        new_event = Event.objects.filter(event_name='test event logged in')[0]
        self.assertEqual(new_event.author, self.test_user)

    def test_correct_redirect_after_create(self):
        response = self.login_and_create_event()
        new_event = Event.objects.filter(event_name='test event logged in')[0]
        self.assertRedirects(response, new_event.get_absolute_url())


class EventUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = make_user(username='testuser', password='12345')
        cls.test_fake_user = make_user(username='fakeuser', password='12345')

    def setUp(self):
        self.client.logout()
        self.test_event = make_event(
            event_name="update test event", author=self.test_user)

    def tearDown(self):
        self.test_event.delete()

    def login_and_update_event(self):
        self.client.login(username='testuser', password='12345')
        return self.client.post(reverse('eventFinder:update', kwargs={'pk': self.test_event.pk}), {
            'event_name': 'updated name',
            'event_type': 'Academic',
            'event_description': 'testevent',
            'event_time': '11/23/2020 23:32',
            'address': 'University of Virginia'
        })

    def test_redirect_when_not_logged_in(self):
        response = self.client.get(
            reverse('eventFinder:update', kwargs={'pk': self.test_event.pk}))
        self.assertRedirects(response, reverse(
            'login')+'?next='+reverse('eventFinder:update', kwargs={'pk': self.test_event.pk}))

    def test_deny_access_when_logged_in_with_different_account(self):
        self.client.login(username='fakeuser', password='12345')
        response = self.client.get(
            reverse('eventFinder:update', kwargs={'pk': self.test_event.pk}))
        self.assertEqual(response.status_code, 403)

    def test_can_update_with_correct_account(self):
        self.login_and_update_event()
        self.assertTrue(Event.objects.filter(
            event_name='updated name').exists())
        self.assertFalse(Event.objects.filter(
            event_name='update test event').exists())

    def test_correct_redirect_after_update(self):
        response = self.login_and_update_event()
        self.assertRedirects(response, reverse(
            'eventFinder:show', kwargs={'pk': self.test_event.pk}))

class EventDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = make_user(username='testuser', password='12345')
        cls.test_fake_user = make_user(username='fakeuser', password='12345')

    def setUp(self):
        self.client.logout()
        self.test_event = make_event(
            event_name="update test event", author=self.test_user)

    def tearDown(self):
        self.test_event.delete()

    def test_redirect_when_not_logged_in(self):
        response = self.client.get(
            reverse('eventFinder:delete', kwargs={'pk': self.test_event.pk}))
        self.assertRedirects(response, reverse(
            'login')+'?next='+reverse('eventFinder:delete', kwargs={'pk': self.test_event.pk}))

    def test_deny_access_when_logged_in_with_different_account(self):
        self.client.login(username='fakeuser', password='12345')
        response = self.client.get(
            reverse('eventFinder:delete', kwargs={'pk': self.test_event.pk}))
        self.assertEqual(response.status_code, 403)

    def test_can_delete_with_correct_account(self):
        self.client.login(username='testuser', password='12345')
        self.assertTrue(Event.objects.filter(
            event_name='update test event').exists())
        
        self.client.post(reverse('eventFinder:delete', kwargs={'pk': self.test_event.pk}))

        self.assertFalse(Event.objects.filter(
            event_name='update test event').exists())

    def test_correct_redirect_after_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('eventFinder:delete', kwargs={'pk': self.test_event.pk}))
        self.assertRedirects(response, reverse('eventFinder:index'))


class EventAttendViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = make_user(username='testuser', password='12345')
        cls.test_attendee1 = make_user(username='attendee1', password='12345')
        cls.test_attendee2 = make_user(username='attendee2', password='12345')

    def setUp(self):
        self.client.logout()
        self.test_event = make_event(
            event_name="update test event", author=self.author)

    def tearDown(self):
        self.test_event.delete()

    def test_show_has_attend_button(self):
        response = self.client.get(reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))

    def test_correct_attend_button_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))
        self.assertRedirects(response, reverse('login')+'?next='+reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))

    def test_attend_button_addes_user_to_attendees_when_logged_in(self):
        self.client.login(username='attendee1', password='12345')
        response = self.client.get(reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))
        self.assertTrue(self.test_event.attendees.filter(pk=self.test_attendee1.pk).exists())

    def test_show_has_cancel_button_when_in_attendees(self):
        self.client.login(username='attendee1', password='12345')

        # should have attend but not cancel when not attending
        response = self.client.get(reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse('eventFinder:cancel', kwargs={"pk": self.test_event.pk}))

        # attend event
        self.client.get(reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))

        # should have cancel but not attend when attending
        response = self.client.get(reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse('eventFinder:cancel', kwargs={"pk": self.test_event.pk}))

        # cancel attendence
        self.client.get(reverse('eventFinder:cancel', kwargs={"pk": self.test_event.pk}))
        response = self.client.get(reverse('eventFinder:show', kwargs={"pk": self.test_event.pk}))
        self.assertContains(response, reverse('eventFinder:attend', kwargs={"pk": self.test_event.pk}))
        self.assertNotContains(response, reverse('eventFinder:cancel', kwargs={"pk": self.test_event.pk}))