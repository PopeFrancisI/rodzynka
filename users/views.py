from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


# Create your views here.
from users.forms import ExtendedUserCreationForm


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
