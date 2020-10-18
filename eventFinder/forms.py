from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_name',)
        widgets = {
            'event_name': forms.Textarea(attrs={'class': 'form-control'}),
        }