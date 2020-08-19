from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from family.models import Family


# Create your views here.
class FamilyMainView(LoginRequiredMixin, View):

    def get(self, request, slug):
        user_families = Family.objects.filter(user=self.request.user)
        family = Family.objects.get(slug=slug)

        context = {'user_families': user_families}

        return render(request, 'family_main.html', context)


class FamilyPickView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user_families = Family.objects.filter(user=self.request.user)

        if len(user_families) == 1:
            return redirect(reverse('family_main', args=(user_families.first().slug, )))

        context = {'user_families': user_families}

        return render(request, 'family_pick.html', context)

