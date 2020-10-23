from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

from family.models import Family


class Calendar(models.Model):
    name = models.CharField(max_length=64)
    is_main = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


def create_calendar(name, family, is_main=False, users=None):

    if is_main:
        users = family.user.all()

    calendar = Calendar.objects.create(
        name=name,
        is_main=is_main,
        family=family,
    )
    calendar.users.set(users)

    calendar.save()

    return calendar


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(default='')
    date = models.DateTimeField()
    is_all_day = models.BooleanField(default=True)
    is_important = models.BooleanField(default=False, verbose_name='Important')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)


def get_incoming_events(family, n=5):
    try:
        family_main_calendar = Calendar.objects.get(family=family, is_main=True)
        incoming_events = Event.objects.filter(
            calendar=family_main_calendar,
            date__gte=datetime.now()
        ).order_by('-date')[:n]
    except Exception:
        incoming_events = None

    return incoming_events
