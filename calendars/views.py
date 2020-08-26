from calendar import monthrange
from collections import defaultdict
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, Form
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, FormView, DeleteView, UpdateView

from calendars.forms import CalendarAddUserForm
from calendars.models import Event, Calendar, create_calendar
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

months_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}


class Day:
    """
    Container class for day data. Instance of this class holds data about
    day number, day of the week name and all events having place that day.
    """
    def __init__(self, day_number, day_of_week, events):
        self.day_number = day_number
        self.day_of_week = day_of_week
        self.events = events


class CalendarDetailView(LoginRequiredMixin, GetUserFamilyMixin, View):
    """
    Shows a calendar with its events.
    """
    def get(self, request, family_slug, calendar_pk=None, year=None, month=None):
        """
        Renders calendar details page.
        :param request:
        :param family_slug:
        :param calendar_pk:
        :param year:
        :param month:
        :return:
        """
        family = self.get_family(request.user, family_slug)
        user_calendars = request.user.calendar_set.filter(family=family)

        if calendar_pk is None:
            calendar_pk = family.calendar_set.get(is_main=True).id
        current_calendar = request.user.calendar_set.get(id=calendar_pk, family=family)

        year_month_tuple = self.date_to_int(year, month)
        year = year_month_tuple[0]
        month = year_month_tuple[1]

        month_data = monthrange(int(year), int(month))
        month_events = current_calendar.event_set.filter(date__month=month)
        days_dict = defaultdict(list)

        for event in month_events:
            day_number = event.date.day
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
                   'day_data': days_list,
                   'months_all': months_dict}

        return render(request, 'calendar_detail.html', context)

    def post(self, request, family_slug, calendar_pk=None, year=None, month=None):
        """
        Redirects to calendar for provided year and month. Used by date selection on page.
        :param request:
        :param family_slug:
        :param calendar_pk:
        :param year:
        :param month:
        :return:
        """
        year = request.POST.get('year')
        month = request.POST.get('month')
        if year and month:
            return redirect(reverse('calendar_detail', args=(family_slug, self.kwargs['calendar_pk'], year, month)))
        else:
            return redirect(reverse('calendar_detail', args=(family_slug, self.kwargs['calendar_pk'])))

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


class CalendarCreateView(LoginRequiredMixin, GetUserFamilyMixin, CreateView):
    model = Calendar
    fields = ['name']
    template_name = 'calendar_create.html'

    def get_success_url(self):
        return reverse('calendar_detail', args=(self.kwargs['family_slug'], ))

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        user = self.request.user
        family = self.get_family(user, self.kwargs['family_slug'])
        create_calendar(name, family, False, (user, ))

        return redirect(self.get_success_url())


class CalendarSetUsersView(LoginRequiredMixin, GetUserFamilyMixin, FormView):
    form_class = CalendarAddUserForm
    template_name = 'calendar_set_users.html'

    def get_success_url(self):
        return reverse('calendar_detail', args=(self.kwargs['family_slug'], self.kwargs['calendar_pk']))

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        user = self.request.user
        family = self.get_family(user, self.kwargs['family_slug'])
        form = form_class(user, family, **self.get_form_kwargs())
        calendar = user.calendar_set.get(id=self.kwargs['calendar_pk'])
        form.initial = {'users': calendar.users.all()}
        return form

    def form_valid(self, form):
        """
        Adds users to the calendar and redirects to calendar page.
        :param form:
        :return:
        """
        calendar = self.request.user.calendar_set.get(id=self.kwargs['calendar_pk'])

        if calendar.is_main:
            return redirect(self.get_success_url())

        users = list(form.cleaned_data['users'])
        users.append(self.request.user)
        calendar.users.set(users)

        calendar.save()

        return redirect(self.get_success_url())


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'is_important']
    template_name = 'event_create.html'

    def get_success_url(self):
        return reverse('calendar_detail',
                       args=(self.kwargs['family_slug'],
                             self.kwargs['calendar_pk'],
                             self.kwargs['year'],
                             self.kwargs['month']))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].required = False
        return form

    def form_valid(self, form):

        form: ModelForm
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        is_important = form.cleaned_data.get('is_important')

        time = self.request.POST.get('time')
        if time:
            split_time = time.split(':')
            hour = int(split_time[0])
            minute = int(split_time[1])
            is_all_day = False
        else:
            hour = 0
            minute = 0
            is_all_day = True

        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        day = int(self.kwargs['day'])

        date = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )

        creator = self.request.user
        calendar = Calendar.objects.get(id=self.kwargs['calendar_pk'])

        event = Event(
            title=title,
            description=description,
            is_important=is_important,
            is_all_day=is_all_day,
            date=date,
            creator=creator,
            calendar=calendar
        )

        event.save()

        return redirect(self.get_success_url())


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'is_important']
    template_name = 'event_update.html'
    pk_url_kwarg = 'event_pk'

    def get_success_url(self):
        return reverse('calendar_detail',
                       args=(self.kwargs['family_slug'],
                             self.kwargs['calendar_pk'],
                             self.kwargs['year'],
                             self.kwargs['month']))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].required = False
        return form

    def form_valid(self, form):
        event = self.get_object()
        if event.creator is not self.request.user:
            return redirect(self.get_success_url())
        else:
            return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_delete.html'
    pk_url_kwarg = 'event_pk'

    def get_success_url(self):
        return reverse('calendar_detail',
                       args=(self.kwargs['family_slug'],
                             self.kwargs['calendar_pk'],
                             self.kwargs['year'],
                             self.kwargs['month']))

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        if event.creator is not request.user:
            return redirect(self.get_success_url())
        else:
            return super(EventDeleteView, self).delete(request, *args, **kwargs)