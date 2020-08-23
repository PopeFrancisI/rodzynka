from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, DeleteView
from gallery.forms import GalleryMediaCreateForm
from gallery.models import Gallery, Media
from family.views import GetUserFamilyMixin


# Create your views here.
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

        paginator = Paginator(medias, 10)
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

        print('image title: ' + image.title)
        if not image.title:
            image.title = image.image.name

        if image.galleries:
            galleries = image.galleries.all()
            for gallery in galleries:
                gallery.last_image_upload_date = image.upload_date

        image.galleries.add(Gallery.objects.get(id=self.kwargs['gallery_pk']))
        image.save()
        return redirect(reverse('gallery_detail', args=(self.kwargs['family_slug'], self.kwargs['gallery_pk'])))


class GalleryMediaDeleteView(LoginRequiredMixin, DeleteView):
    model = Media
    template_name = 'gallery_media_delete.html'
    pk_url_kwarg = 'media_pk'

    def get_success_url(self):
        """
        get_succes_url override that redirects to gallery_detail page
        :return:
        """
        return reverse_lazy('gallery_detail', args=(self.kwargs['family_slug'], self.kwargs['gallery_pk']))

    def delete(self, request, *args, **kwargs):
        """
        delete override that also deletes actual media file
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.get_object().image.delete()
        return super().delete(request, *args, **kwargs)
