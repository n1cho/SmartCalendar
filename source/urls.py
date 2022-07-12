from django.urls import path

from . import views

urlpatterns = [
    #home page
    path('',views.index,name='index'),
    path('new_calend/',views.new_calend,name='new_calend')
]