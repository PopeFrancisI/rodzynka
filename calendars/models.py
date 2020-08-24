from django.contrib.auth.models import User
from django.db import models

from family.models import Family


class Calendar(models.Model):
    name = models.CharField(max_length=64)
    is_main = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class EventDateTimeField(models.DateTimeField):

    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(default='')
    date_from = models.DateTimeField()
    date_to = models.DateTimeField(null=True)
    is_important = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
