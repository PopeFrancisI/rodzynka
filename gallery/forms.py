from django.forms import ModelForm
from django import forms
from gallery.models import Media


class GalleryMediaCreateForm(ModelForm):
    title = forms.CharField(max_length=32, label='Image title')

    class Meta:
        model = Media
        fields = ['title', 'image']
