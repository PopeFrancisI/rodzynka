from django.contrib.auth.models import User
from django.forms import Form
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from family.forms import FamilyCreateForm
from family.models import Family
from family.utils import slugify
from gallery.models import Gallery, create_gallery


class GetUserFamilyMixin:
    def get_family(self, user, slug):
        families = user.family_set.all()
        family = families.get(slug=slug)
        return family


def get_newest_media(family):
    """
    returns a tuple where first value is the newest media/image from family gallery,
    and the second value is the gallery containing that media/image.
    :param family:
    :return:
    """
    last_updated_gallery = family.gallery_set.all().order_by('last_media_upload_date').first()
    try:
        newest_media = last_updated_gallery.media_set.latest('upload_date')
    except Exception:
        newest_media = None
    return newest_media, last_updated_gallery


def get_newest_wishes(family, n=5):
    """
    returns n newest family wishes
    :param family:
    :param n: number of wishes to be returned
    :return:
    """
    family: Family
    try:
        newest_wishes = family.wish_set.order_by('-create_date')[:n]
    except Exception:
        newest_wishes = None

    return newest_wishes


class FamilyMainView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        family = self.get_family(request.user, family_slug)

        newest_media_results = get_newest_media(family)
        newest_media = newest_media_results[0]
        newest_media_gallery = newest_media_results[1]

        newest_wishes = get_newest_wishes(family)

        context = {'user_family': family,
                   'newest_media': newest_media,
                   'newest_media_gallery': newest_media_gallery,
                   'newest_wishes': newest_wishes}
        request.session['current_family_slug'] = family.slug

        return render(request, 'family_main.html', context)


class FamilyPickView(LoginRequiredMixin, View):

    def get(self, request):
        user_families = Family.objects.filter(user=self.request.user)

        if len(user_families) == 1:
            return redirect(reverse('family_main', args=(user_families.first().slug, )))

        return render(request, 'family_pick.html')


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class FamilyCreateView(FormView):
    form_class = FamilyCreateForm
    template_name = 'family_create.html'
    success_url = reverse_lazy('family_pick')

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        last_name = form.cleaned_data.get('last_name')
        slug = slugify(name)
        user = self.request.user
        family = Family.objects.create(name=name,
                                       last_name=last_name,
                                       slug=slug)
        family.user.add(user)
        family.save()

        create_gallery(f'Main gallery', family, True)

        # create wishlist
        # create calendar

        return super().form_valid(form)
