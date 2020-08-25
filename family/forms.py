from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django import forms
from family.models import Family
from family.validators import validate_user_exists


class FamilyCreateForm(ModelForm):

    name = forms.CharField(max_length=32, label='family nickname', required=True)
    last_name = forms.CharField(max_length=32, label='family last name', required=True)

    class Meta:
        model = Family
        fields = ['name', 'last_name']


class FamilyInviteForm(Form):
    username = forms.CharField(max_length=150,
                               required=True,
                               help_text='Username is case-sensitive',
                               validators=[validate_user_exists])

    class Meta:
        fields = ['username']
