from django import forms
from .models import Event
from bootstrap_datepicker_plus import DateTimePickerInput
from address.widgets import AddressWidget


EVENT_TYPE_CHOICES = (('Academic', 'Academic'), ('Sports', 'Sports'), ('Social', 'Social'), ('Political', 'Political'))

class MyDateTimePickerInput(DateTimePickerInput):
    template_name = 'eventFinder/date-picker.html'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = ('event_name', 'event_date', 'event_description', 'event_type')
        fields = ('event_name', 'event_date', 'event_description', 'event_type', 'address')
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': MyDateTimePickerInput(attrs={'class': 'form-control d-inline-block', 'id': 'calendar'}),
            'event_description': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(choices=EVENT_TYPE_CHOICES, attrs={'class': 'form-control'}),
            'address': AddressWidget(attrs={'required':'true','class': 'form-control'})
        }