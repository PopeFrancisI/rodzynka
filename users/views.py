from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View


# Create your views here.
class SignupView(View):

    def post(self, request):
        form = UserCreationForm()
        return render(request, 'registration.html', {'form': form})