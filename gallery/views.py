from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView

from family.models import Family
from gallery.forms import GalleryMediaCreateForm
from gallery.models import Gallery, Media
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

        context = {'page_obj': page_obj, 'family': family, 'gallery': gallery}
        return render(request, 'gallery_detail.html', context)


class GalleryMediaCreateView(LoginRequiredMixin, FormView):
    form_class = GalleryMediaCreateForm
    success_url = reverse_lazy('family_pick')
    template_name = 'gallery_media_add.html'

    def form_valid(self, form):
        image = form.save()
        image: Media
        image.uploader = self.request.user

        if not image.title:
            image.title = image.image.name

        if image.galleries:
            galleries = image.galleries.all()
            for gallery in galleries:
                gallery.last_image_upload_date = image.upload_date

        image.galleries.add(Gallery.objects.get(id=self.kwargs['pk']))
        return super().form_valid(form)
