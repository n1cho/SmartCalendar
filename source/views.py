from calendar import calendar
from django.shortcuts import render


from .models import Calendar

def index(request):
    if request.user.is_authenticated:
        calendars = Calendar.objects.filter(members=request.user).order_by('name')
        context = {'calendars':calendars}
    else:
        context = {}
    return render(request,'page/index.html',context)