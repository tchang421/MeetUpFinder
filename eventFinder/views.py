from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.utils import timezone

from .models import Event
from .forms import EventForm



def index(request):
    context = {}
    if request.user.is_authenticated:
        context['logged_in']=True
    else:
        context['logged_in']=False

    return render(request,'eventFinder/index.html',context)

class EventListView(generic.ListView):
    template_name = 'eventFinder/list.html'
    context_object_name = 'event_list'
    def get_queryset(self):
        return Event.objects.all()

class CreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/create.html'

class NewView(View):
    def get(self, request):
        return render(request,'eventFinder/new.html')

def creating(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
    return HttpResponseRedirect(reverse('eventFinder:list'))

