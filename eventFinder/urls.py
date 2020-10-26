from django.urls import path
from . import views

app_name = 'eventFinder'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.NewView.as_view(), name='create'),
    path('<int:pk>', views.ShowView.as_view(), name='show'),
    path('<int:pk>/edit', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.DeleteView.as_view(), name='delete'),
]
