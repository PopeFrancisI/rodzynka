from calendar import monthrange
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from family.views import GetUserFamilyMixin


days_of_week = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}


class Day:
    def __init__(self, day_number, day_of_week, events):
        self.day_number = day_number
        self.day_of_week = day_of_week
        self.events = events


class CalendarDetailView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug, calendar_pk, year=None, month=None):

        family = self.get_family(request.user, family_slug)
        user_calendars = request.user.calendar_set.filter(family=family)
        current_calendar = request.user.calendar_set.get(id=calendar_pk, family=family)

        year_month_tuple = self.date_to_int(year, month)
        year = year_month_tuple[0]
        month = year_month_tuple[1]

        month_data = monthrange(int(year), int(month))
        month_events = current_calendar.event_set.filter(date_from__month=month)
        days_dict = defaultdict(list)

        for event in month_events:
            day_number = event.date_from.day
            days_dict[day_number].append(event)

        days_list = []
        day_of_week = month_data[0]

        for day in range(1, month_data[1] + 1):
            day_obj = Day(day, days_of_week[day_of_week], days_dict.get(day))
            days_list.append(day_obj)
            day_of_week += 1
            if day_of_week > 6:
                day_of_week = 1

        context = {'family': family,
                   'current_calendar': current_calendar,
                   'user_calendars': user_calendars,
                   'year': year,
                   'month': month,
                   'day_data': days_list}

        return render(request, 'calendar_detail.html', context)

    @staticmethod
    def date_to_int(year, month):
        if year is None:
            year = timezone.now().year
        else:
            year = int(year)
        if month is None:
            month = timezone.now().month
        else:
            month = int(month)
        return year, month

