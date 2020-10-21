from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView

from .forms import EventForm
from .models import Event


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'events':Event.objects.all(),
            'user':request.user
        }
        return render(request,'eventFinder/index.html',context)
    
    # @login_required(login_url=settings.LOGIN_URL)
    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.author = request.user
            new_event.save();
        return redirect(reverse('eventFinder:index'))

class NewView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/new.html'


