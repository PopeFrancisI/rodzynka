from django.contrib import admin

from calendars.models import Event, Calendar

admin.site.register(Event)
admin.site.register(Calendar)