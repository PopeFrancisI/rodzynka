from django.contrib import admin

# Register your models here.
from family.models import Family
from gallery.models import Gallery, Media

admin.site.register(Family)
admin.site.register(Gallery)
admin.site.register(Media)