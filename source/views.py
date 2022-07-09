from django.shortcuts import render

from .models import Calendar

def index(request):
    return render(request,'page/index.html')