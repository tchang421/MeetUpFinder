from django import forms
from .models import Event
from bootstrap_datepicker_plus import DateTimePickerInput

class MyDateTimePickerInput(DateTimePickerInput):
    template_name = 'eventFinder/date-picker.html'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_date', 'event_description')
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': MyDateTimePickerInput(attrs={'class': 'form-control d-inline-block', 'id': 'calendar'}),
            'event_description': forms.TextInput(attrs={'class': 'form-control'})
        }