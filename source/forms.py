from django import forms

from .models import Calendar,Notification

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

class CreateNotification(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text','data_to_notf']
        labels = {'text':'Text notification','data_to_notf':'Date'}