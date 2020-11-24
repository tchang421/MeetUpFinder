from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core.serializers import serialize

from .forms import EventForm
from .models import Event

ordering_name_to_field = {
    'Name': 'event_name', 
    'Event Time': 'event_date', 
    'Publish Time': 'pub_date',
}

class IndexView(ListView):
    model = Event
    context_object_name="events"
    template_name="eventFinder/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderings'] = ordering_name_to_field
        return context
    
    def get_queryset(self):
        ordering = self.request.GET.get('ordering')
        if not ordering:
            ordering = ordering_name_to_field['Name']
        return Event.objects.all().order_by(ordering)

class NewView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ShowView(DetailView):
    model = Event
    template_name='eventFinder/show.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_json"] = serialize('json', [self.get_object()])
        return context
    


class UpdateView(UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/form.html'
    def test_func(self):
        return self.get_object().author == self.request.user

class DeleteView(UserPassesTestMixin,DeleteView):
    model = Event
    template_name="eventFinder/delete.html"
    success_url = reverse_lazy('eventFinder:index')
    def test_func(self):
        return self.get_object().author == self.request.user

class AttendView(LoginRequiredMixin, RedirectView):
    pattern_name ="eventFinder:show"

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        event.add_attendee(self.request.user)
        return super().get_redirect_url(*args, **kwargs)

class CancelView(RedirectView):
    pattern_name ="eventFinder:show"
    
    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        event.remove_attendee(self.request.user)
        return super().get_redirect_url(*args, **kwargs)

