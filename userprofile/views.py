from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import UserProfile
from .forms import UserProfileForm
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.

class ProfileDisplay(DetailView):
    model = UserProfile
    template_name = 'userprofile/show.html'
    context_object_name = 'User'

class ShowView(DetailView):
    model = UserProfile
    template_name='userprofile/show.html'

class UpdateView(TemplateView):
    form = UserProfileForm
    template_name = 'userprofile/edit.html'

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home', kwargs={'pk': pk}))
        context = self.get_context_data(form=form)
        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
'''

class UpdateView(UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'userprofile/edit.html'
    def test_func(self):
        print(self.request.user)
        return self.request.user.profile.id == self.kwargs['pk']

    def post(self, request, **kwargs):
        form = UserProfileForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
        else:
            form = UserProfileForm()
        return render(request, self.template_name, {"form": form, "pk":self.request.user.profile.id })

'''