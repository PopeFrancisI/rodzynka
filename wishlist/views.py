from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.forms import Form
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from family.models import Family
from family.views import GetUserFamilyMixin
from wishlist.models import Wish


class WishlistView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        family = self.get_family(request.user, family_slug)
        context = {}
        family: Family
        try:
            wishlist = defaultdict(list)
            for wish in family.wish_set.all():
                wishlist[f'{wish.user.username} ({wish.user.first_name} {wish.user.last_name})'].append(wish)

            wishlist = list(wishlist.items())
            context['wishlist'] = wishlist
        except Exception:
            context['wishlist'] = None

        context['family'] = family
        context['current_user'] = f'{request.user.username} ({request.user.first_name} {request.user.last_name})'
        return render(request, 'wishlist.html', context)


def wishlist_success_url(view):
    return reverse_lazy('wishlist', args=(view.kwargs['family_slug'],))


class WishCreateView(LoginRequiredMixin, CreateView):
    model = Wish
    template_name = 'wish_create.html'
    fields = ['title', 'description', 'is_important']

    def get_form(self, form_class=None):
        form = super(WishCreateView, self).get_form(form_class)
        form.fields['is_important'].widget = forms.CheckboxInput()
        return form

    def get_success_url(self):
        return wishlist_success_url(self)

    def form_valid(self, form):
        form: Form
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        is_important = form.cleaned_data.get('is_important')
        family = Family.objects.get(slug=self.kwargs['family_slug'])
        user = self.request.user
        try:
            Wish.objects.create(title=title,
                                description=description,
                                is_important=is_important,
                                family=family,
                                user=user)
        except Exception:
            pass

        return redirect(self.get_success_url())


class WishDeleteView(LoginRequiredMixin, DeleteView):
    model = Wish
    template_name = 'wish_delete.html'
    pk_url_kwarg = 'wish_pk'

    def get_success_url(self):
        return wishlist_success_url(self)

    def delete(self, request, *args, **kwargs):
        wish = self.get_object()
        if wish.user != request.user:
            return redirect(self.get_success_url())
        else:
            return super(WishDeleteView, self).delete(request, *args, **kwargs)


class WishUpdateView(LoginRequiredMixin, UpdateView):
    model = Wish
    template_name = 'wish_update.html'
    pk_url_kwarg = 'wish_pk'
    fields = ['title', 'description', 'is_important']

    def get_form(self, form_class=None):
        form = super(WishUpdateView, self).get_form(form_class)
        form.fields['is_important'].widget = forms.CheckboxInput()
        return form

    def get_success_url(self):
        return wishlist_success_url(self)

    def form_valid(self, form):
        if self.object.user != self.request.user:
            return redirect(self.get_success_url())
        else:
            return super().form_valid(form)

