from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import UserProfile
from .forms import UserProfileForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.


class ShowView(DetailView):
    model = UserProfile
    template_name='userprofile/show.html'

class UpdateView(UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'userprofile/edit.html'
    def test_func(self):
        return self.request.user.profile.id == self.kwargs['pk']