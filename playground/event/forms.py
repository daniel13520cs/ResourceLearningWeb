# forms.py
from django import forms
from .models import Event

class EventForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(required=False, widget=forms.Textarea)
    startTime = forms.DateTimeField(required=True)
    location = forms.CharField(max_length=255, required=False)
    URL = forms.URLField(required=False)
