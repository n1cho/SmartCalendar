from django import forms

from .models import Calendar

class NewCalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name']
        labels = {'name': 'Name Calendar'}

class EnterToCalendar(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['code']
        labels = {'code':'Enter code'}