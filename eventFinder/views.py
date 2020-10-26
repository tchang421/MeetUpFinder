from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import EventForm
from .models import Event


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'events':Event.objects.all(),
        }
        return render(request,'eventFinder/index.html',context)
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.author = request.user
            new_event.save();
        return redirect(reverse('eventFinder:index'))

class NewView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/form.html'

class ShowView(DetailView):
    model = Event
    template_name='eventFinder/show.html'


class UpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/form.html'

    def get_success_url(self) -> str:
        return reverse('eventFinder:show', kwargs={'pk': self.object.id})


