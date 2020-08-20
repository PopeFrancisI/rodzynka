from django.shortcuts import render
from django.views import View


# Create your views here.
class GalleryPickView(View):

    def get(self, request, family_slug):
        return render(request, 'gallery_pick.html')
