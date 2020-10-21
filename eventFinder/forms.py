from django import forms
from .models import Event
from bootstrap_datepicker_plus import DateTimePickerInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_date')
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': DateTimePickerInput(attrs={'class': 'form-control', 'id': 'calendar'})
        }