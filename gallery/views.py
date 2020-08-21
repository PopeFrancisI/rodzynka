from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from family.models import Family
from gallery.models import Gallery
from family.views import GetUserFamilyMixin

# Create your views here.
class GalleryPickView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        family = self.get_family(request.user, family_slug)
        galleries = family.gallery_set.all()
        galleries_with_covers = []
        for gallery in galleries:
            galleries_with_covers.append((gallery, gallery.media_set.first()))
        context = {'family': family, 'galleries': galleries_with_covers}

        return render(request, 'gallery_pick.html', context)


class GalleryDetailView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, pk, family_slug):
        family = self.get_family(request.user, family_slug)
        gallery = Gallery.objects.get(pk=pk, family=family)
        medias = gallery.media_set.all().order_by('-upload_date')

        paginator = Paginator(medias, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'family': family}
        return render(request, 'gallery_detail.html', context)
