from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


# Create your views here.
from django.views.generic import FormView

from family.models import Family
from users.forms import ExtendedUserCreationForm, FamilyRequestJoinForm


class SignupView(View):

    def get(self, request):
        form = ExtendedUserCreationForm()
        return render(request, 'registration/registration.html', {'form': form})

    def post(self, request):
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect(reverse('family_pick'))
        return render(request, 'registration/registration.html', {'form': form})


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
