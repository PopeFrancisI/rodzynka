from django.shortcuts import render
from django.views import View

# Create your views here.
class FamilyMainView(View):

    def get(self, request):
        context = {'testo': 'test context'}
        return render(request, 'family_main.html', context)