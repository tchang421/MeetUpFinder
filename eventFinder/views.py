from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone

from .models import Event


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


