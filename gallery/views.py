from copy import copy, deepcopy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, DeleteView, CreateView

from family.models import Family
from gallery.forms import GalleryMediaCreateForm
from gallery.models import Gallery, Media, create_gallery, get_newest_media_in_gallery
from family.views import GetUserFamilyMixin


class GalleryPickView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        """
        get all family's galleries and render the family gallery page
        :param request:
        :param family_slug:
        :return:
        """
        family = self.get_family(request.user, family_slug)
        galleries = family.gallery_set.all()
        galleries_with_covers = []
        for gallery in galleries:
            gallery_obj = gallery
            gallery_cover = gallery.media_set.latest('upload_date') if gallery.media_set.first() else None
            galleries_with_covers.append((gallery_obj, gallery_cover))
        context = {'family': family, 'galleries': galleries_with_covers}

        return render(request, 'gallery_pick.html', context)


class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = Gallery
    fields = ['name']
    template_name = 'gallery_create.html'

    def get_success_url(self):
        return reverse_lazy('gallery_pick', args=(self.kwargs['family_slug'], ))

    def form_valid(self, form):
        """
        creates a new non-main gallery
        :param form:
        :return:
        """
        name = form.cleaned_data.get('name')
        creator = self.request.user
        family = Family.objects.get(slug=self.kwargs['family_slug'])
        create_gallery(name, family, False, creator)

        return redirect(self.get_success_url())


class GalleryDeleteView(LoginRequiredMixin, DeleteView):
    model = Gallery
    template_name = 'gallery_delete.html'
    pk_url_kwarg = 'gallery_pk'

    def get_success_url(self):
        """
        get_succes_url override that redirects to gallery_pick page
        :return:
        """
        return reverse_lazy('gallery_pick', args=(self.kwargs['family_slug'], ))

    def delete(self, request, *args, **kwargs):
        """
        Deletes gallery and its all images unless it's a main gallery
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        gallery = self.get_object()

        if gallery.is_main:
            return redirect(self.get_success_url())

        if gallery.creator != request.user:
            return redirect(self.get_success_url())

        gallery_medias = self.get_object().media_set.all()
        for media in gallery_medias:
            media.delete()
        return super().delete(request, *args, **kwargs)


class GalleryDetailView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, gallery_pk, family_slug):
        """
        get gallery data and render a this gallery's page
        :param request:
        :param gallery_pk:
        :param family_slug:
        :return:
        """
        family = self.get_family(request.user, family_slug)
        gallery = Gallery.objects.get(pk=gallery_pk, family=family)
        medias = gallery.media_set.all().order_by('-upload_date')

        paginator = Paginator(medias, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'family': family, 'gallery': gallery}
        return render(request, 'gallery_detail.html', context)


class GalleryMediaCreateView(LoginRequiredMixin, FormView):
    form_class = GalleryMediaCreateForm
    template_name = 'gallery_media_add.html'

    def form_valid(self, form):
        """
        create media and attach it to a gallery and set gallery's last update date to medias creation date
        :param form:
        :return:
        """
        image = form.save()
        image.uploader = self.request.user

        if not image.title:
            image.title = image.image.name

        current_gallery = Gallery.objects.get(id=self.kwargs['gallery_pk'])
        image.galleries.add(current_gallery)

        galleries = image.galleries.all()
        for gallery in galleries:
            gallery.last_media_upload_date = image.upload_date
        galleries.bulk_update(galleries, ['last_media_upload_date'])

        image.save()

        return redirect(reverse('gallery_detail', args=(self.kwargs['family_slug'], self.kwargs['gallery_pk'])))


class GalleryMediaDeleteView(LoginRequiredMixin, DeleteView):
    model = Media
    template_name = 'gallery_media_delete.html'
    pk_url_kwarg = 'media_pk'

    def get_success_url(self):
        """
        get_success_url override that redirects to gallery_detail page
        :return:
        """
        return reverse_lazy('gallery_detail', args=(self.kwargs['family_slug'], self.kwargs['gallery_pk']))

    def delete(self, request, *args, **kwargs):
        """
        Deletes media if logged user is the uploader of the media
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        media = self.get_object()

        if media.uploader != request.user:
            return redirect(self.get_success_url())

        try:
            galleries = media.galleries.all()

            galleries = copy(galleries)

            media.delete()
            print(galleries)

            for gallery in galleries:
                newest_media = get_newest_media_in_gallery(gallery)
                if newest_media:
                    gallery.last_media_upload_date = newest_media.upload_date
                else:
                    gallery.last_media_upload_date = None
                gallery.save()

        except Exception as e:
            print(e)

        return redirect(self.get_success_url())
