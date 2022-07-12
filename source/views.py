from calendar import calendar
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User


from .models import Calendar
from .forms import CalendarForm

def index(request):
    if request.user.is_authenticated:
        calendars = Calendar.objects.filter(members=request.user).order_by('name')
        context = {'calendars':calendars}
    else:
        context = {}
    return render(request,'page/index.html',context)

def new_calend(request):
    user = User.objects.get(id=request.user.id)
    if request.method != 'POST':
        form = CalendarForm()
    else:
        form = CalendarForm(request.POST)
        if form.is_valid():
            new_calendar = form.save(commit=False)
            new_calendar.code = User.objects.make_random_password(8)
            new_calendar.owner = request.user
            new_calendar.save()
            new_calendar.members.add(user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form':form,'user':user}
    return render(request,'page/new_calend.html',context)