from django.contrib.auth.models import User
from django.db import models

from family.models import Family


class Calendar(models.Model):
    name = models.CharField(max_length=64)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(default='')
    is_important = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)