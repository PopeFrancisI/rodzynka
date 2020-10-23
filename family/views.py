from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from calendars.models import create_calendar, get_incoming_events
from family.forms import FamilyCreateForm, FamilyInviteForm, FamilyRequestJoinForm
from family.models import Family
from family.utils import slugify
from gallery.models import create_gallery, get_newest_media
from wishlist.models import get_newest_wishes


class GetUserFamilyMixin:
    def get_family(self, user, slug):
        families = user.family_set.all()
        family = families.get(slug=slug)
        return family


class FamilyMainView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        family = self.get_family(request.user, family_slug)

        newest_media_results = get_newest_media(family)
        newest_media = newest_media_results[0]
        newest_media_gallery = newest_media_results[1]

        newest_wishes = get_newest_wishes(family)

        incoming_events = get_incoming_events(family)

        users_requesting_join = family.requesting_users.all()

        context = {'user_family': family,
                   'newest_media': newest_media,
                   'newest_media_gallery': newest_media_gallery,
                   'newest_wishes': newest_wishes,
                   'incoming_events': incoming_events,
                   'requesting_users': users_requesting_join}
        request.session['current_family_slug'] = family.slug

        return render(request, 'family_main.html', context)


class FamilyPickView(LoginRequiredMixin, View):

    def get(self, request):
        user = self.request.user
        user_families = Family.objects.filter(user=user)

        if len(user_families) == 1:
            return redirect(reverse('family_main', args=(user_families.first().slug, )))

        inviting_families = user.inviting_families.all()

        return render(request, 'family_pick.html', context={'inviting_families': inviting_families})


def family_add_user(family, user):
    family.user.add(user)
    main_calendar = family.calendar_set.get(is_main=True)
    main_calendar.users.add(user)


class FamilyJoinView(LoginRequiredMixin, View):

    def get(self, request, family_slug):
        family = Family.objects.get(slug=family_slug)
        context = {'family': family}

        return render(request, 'family_join.html', context)

    def post(self, request, family_slug):
        family = Family.objects.get(slug=family_slug)

        if request.POST.get('accept'):
            family_add_user(family, request.user)
            return redirect(reverse('family_main', args=(family_slug, )))
        else:
            family.invited_users.remove(request.user)
            return redirect(reverse('family_pick'))


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class FamilyCreateView(LoginRequiredMixin, FormView):
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

        create_gallery(f'main gallery', family, True)
        create_calendar(f'family calendar', family, True)

        return super().form_valid(form)


class FamilyInviteView(LoginRequiredMixin, FormView):
    form_class = FamilyInviteForm
    template_name = 'family_invite.html'

    def get_success_url(self):
        return reverse('family_main', args=(self.kwargs['family_slug'], ))

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data.get('username'))
        family = Family.objects.get(slug=self.kwargs['family_slug'])

        family.invited_users.add(user)

        return redirect(self.get_success_url())


class FamilyRequestJoinView(LoginRequiredMixin, FormView):
    form_class = FamilyRequestJoinForm
    template_name = 'family_request_join.html'

    def get_success_url(self):
        return reverse('family_pick')

    def form_valid(self, form):
        user = self.request.user
        family = Family.objects.get(name=form.cleaned_data.get('name'))

        family.requesting_users.add(user)

        return redirect(self.get_success_url())


class FamilyAddUserView(LoginRequiredMixin, View):
    """
    Adding user to a family by a family member.
    """
    def get(self, request, family_slug, user_pk):
        """
        Renders a page where a family member can decide whether add a new user or not.
        :param request:
        :param family_slug:
        :param user_pk:
        :return:
        """
        family = Family.objects.get(slug=family_slug)
        user = User.objects.get(id=user_pk)
        context = {'family': family, "requesting_user": user}

        return render(request, 'family_add_user.html', context)

    def post(self, request, family_slug, user_pk):
        """
        If join request got accepted, then add new member. Otherwise remove join request.
        :param request:
        :param family_slug:
        :param user_pk:
        :return:
        """
        family = Family.objects.get(slug=family_slug)
        requesting_user = User.objects.get(id=user_pk)

        if request.POST.get('accept'):
            family_add_user(family, requesting_user)
            family.requesting_users.remove(requesting_user)
        else:
            family.requesting_users.remove(requesting_user)

        return redirect(reverse('family_main', args=(family_slug,)))