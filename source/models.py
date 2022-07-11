from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    code = models.CharField(max_length=8)
    owner = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(User,related_name='members')

    def __str__(self):
        return self.name

class Task(models.Model):
    calendar = models.ForeignKey(Calendar,on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=350)
    data_hand_over = models.DateField()
    create_task = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now=True)
    end_task = models.BooleanField()

    def __str__(self):
        if len(self.text) <= 50:
            return self.text
        else:
            return self.text[:50] + "..."

class Notification(models.Model):
    calendar = models.ForeignKey(Calendar,on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=350)
    data_to_notf = models.DateField()
    create_notf = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) <= 50:
            return self.text
        else:
            return self.text[:50] + "..."