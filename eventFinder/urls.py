from django.urls import path

from . import views

app_name = 'eventFinder'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.EventListView.as_view(), name='list'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('creating/', views.creating, name='creating'),
]