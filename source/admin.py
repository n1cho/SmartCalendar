from django.contrib import admin

from source.models import Calendar,Task,Notification

admin.site.register(Calendar)
admin.site.register(Task)
admin.site.register(Notification)