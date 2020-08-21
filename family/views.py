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


class GetUserFamilyMixin:
    def get_family(self, user, slug):
        family = user.family_set.all()
        family = family.get(slug=slug)
        return family


class FamilyMainView(LoginRequiredMixin, GetUserFamilyMixin, View):

    def get(self, request, family_slug):
        family = self.get_family(request.user, family_slug)
        # family = Family.objects.get(slug=family_slug, user__in=[request.user])

        context = {'user_family': family}
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
        form: Form
        name = form.cleaned_data.get('name')
        last_name = form.cleaned_data.get('last_name')
        slug = slugify(name)
        user = self.request.user
        family = Family.objects.create(name=name,
                                       last_name=last_name,
                                       slug=slug)
        family.user.add(user)
        return super().form_valid(form)
