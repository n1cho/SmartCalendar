from calendar import calendar
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User


from .models import Calendar
from .forms import NewCalendarForm,EnterToCalendar

def index(request):
    if request.user.is_authenticated:
        calendars = Calendar.objects.filter(members=request.user).order_by('name')
        context = {'calendars':calendars}
    else:
        context = {}
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