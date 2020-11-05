from django.shortcuts import render
from .models import UserProfile
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
class ShowView(DetailView):
    model = UserProfile
    template_name='userprofile/show.html'