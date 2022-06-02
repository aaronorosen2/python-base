import imp
from django import forms
from .models import Event

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['created_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-group', 'placeholder': 'Enter event name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control form-group', 'placeholder': 'Enter description'}),
            'date': forms.DateInput(attrs={'class': 'form-control form-group', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control form-group', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control form-group', 'type': 'time'}),
        }