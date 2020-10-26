from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import EventForm
from .models import Event


class IndexView(ListView):
    model = Event
    context_object_name="events"
    template_name="eventFinder/index.html"

    # def get(self, request, *args, **kwargs):
    #     if(request.GET.get('datebtn')):
    #         context = {
    #             'events': Event.objects.all().order_by("event_date"),
    #             # 'user':request.user
    #         }
    #     elif(request.GET.get('wordbtn')):
    #         context = {
    #             'events': Event.objects.all().order_by("event_name"),
    #             # 'user':request.user
    #         }
    #     elif(request.GET.get('pubbtn')):
    #         context = {
    #             'events': Event.objects.all().order_by("pub_date"),
    #             # 'user':request.user
    #         }
    #     else:
    #         context = {
    #             'events':Event.objects.all(),
    #             # 'user':request.user
    #         }
    #     return render(request,'eventFinder/index.html',context)
    
    # # @login_required(login_url=settings.LOGIN_URL)
    # def post(self, request, *args, **kwargs):
    #     form = EventForm(request.POST)
    #     if form.is_valid():
    #         new_event = form.save(commit=False)
    #         # new_event.author = request.user
    #         new_event.save()
    #     return redirect(reverse('eventFinder:index'))

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


class UpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'eventFinder/form.html'

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Event
    template_name="eventFinder/delete.html"
    success_url = reverse_lazy('eventFinder:index')
