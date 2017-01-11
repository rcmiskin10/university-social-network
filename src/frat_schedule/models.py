from django.db import models
from accounts.models import MyUser
from frats.models import Frat


class FratSchedule(models.Model):
    user = models.ForeignKey(MyUser)
    frat = models.ForeignKey(Frat)
    path = models.CharField(max_length=350)
    text = models.CharField(max_length=150)
    duedate = models.DateField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-duedate']
    def __unicode__(self):
        return self.user.username

    