from django.shortcuts import render
from django.views import View
from family.models import Family
from gallery.models import Gallery


# Create your views here.
class GalleryPickView(View):

    def get(self, request, family_slug):
        family = Family.objects.get(slug=family_slug)
        galleries = family.gallery_set.all()
        galleries_with_covers = []
        for gallery in galleries:
            galleries_with_covers.append((gallery, gallery.media_set.first()))
        context = {'family': family, 'galleries': galleries_with_covers}

        return render(request, 'gallery_pick.html', context)
