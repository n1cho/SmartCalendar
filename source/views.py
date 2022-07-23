import calendar as calend
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User

import re # regex
from datetime import datetime

from .models import Calendar,Notification
from .forms import NewCalendarForm,EnterToCalendar

def index(request):
    default_calendars = [CreateDefaultCalendar(month=datetime.now().month-1),CreateDefaultCalendar(),CreateDefaultCalendar(month=datetime.now().month+1)]
    if request.user.is_authenticated:
        calendars = Calendar.objects.filter(members=request.user).order_by('name')
        for calendar in calendars:
            notfs = Notification.objects.filter(calendar=calendar).order_by('data_to_notf')
            for default_calendar in default_calendars:
                default_calendar = UpdateCalendarToNotifications(default_calendar,notfs)
        context = {'calendars':calendars,'default_calendars':default_calendars}
    else:
        context = {'default_calendars':default_calendars}
    return render(request,'page/index.html',context)

def edit_members(request):
    id_user = request.GET.get('value')
    user = User.objects.get(id=id_user)
    calendar = Calendar.objects.get(id=request.GET.get('calend'))
    calendar.members.remove(user)
    return HttpResponse('success')

def new_calend(request):
    user = User.objects.get(id=request.user.id)
    if request.method != 'POST':
        form = NewCalendarForm()
    else:
        form = NewCalendarForm(request.POST)
        if form.is_valid():
            new_calendar = form.save(commit=False)
            new_calendar.code = User.objects.make_random_password(8)
            new_calendar.owner = request.user
            new_calendar.save()
            new_calendar.members.add(user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form':form,'user':user}
    return render(request,'page/new_calend.html',context)


def enter_calend(request):
    error = False
    if request.method != 'POST':
        form = EnterToCalendar()
        form_calendar = {}
    else:
        form = EnterToCalendar(request.POST)
        if form.is_valid():
            form_calendar = form.cleaned_data['code']
            try:
                calendar = Calendar.objects.get(code=form_calendar)
                user = User.objects.get(id=request.user.id)
                calendar.members.add(user)
                return HttpResponseRedirect(reverse('index'))
            except:
                error = True
    context = {'form':form,'error': error}
    return render(request,'page/enter_calend.html',context)

def CreateDefaultCalendar(year=datetime.now().year,month=datetime.now().month):
    calendar = {}
    get_calendar_days = calend.Calendar()
    calendar[calend.month_name[month]] = {}
    i = 0
    while i<7:
        calendar[calend.month_name[month]][calend.day_name[i]] = {}
        i+=1
    for days in get_calendar_days.itermonthdays2 (year,month):
        day,week_day = re.findall("\d+", str(days))
        if day != '0':
            calendar[calend.month_name[month]][calend.day_name[int(week_day)]][day] = {}
    return calendar

def UpdateCalendarToNotifications(calendar,notfs):
    get_calendar_days = calend.Calendar()
    if notfs:
        for notf in notfs:
            if notf:
                y,m,d=re.findall("\d+",str(notf.data_to_notf)) # y-year,m-month,d-day
                for days in get_calendar_days.itermonthdays2 (int(y),int(m)):
                    day,week_day = re.findall("\d+", str(days))
                    if calend.month_name[int(m)] in calendar:
                        if int(d) == int(day):
                            calendar[calend.month_name[int(m)]][calend.day_name[int(week_day)]][d]=notf
    return calendar
                