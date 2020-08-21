from django.forms import ModelForm
from django import forms
from family.models import Family


class FamilyCreateForm(ModelForm):

    name = forms.CharField(max_length=32, label='family nickname', required=True)
    last_name = forms.CharField(max_length=32, label='family last name', required=True)

    class Meta:
        model = Family
        fields = ['name', 'last_name']