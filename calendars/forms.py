from django.contrib.auth.models import User
from django.forms import forms, ModelForm, Form
from django import forms


class CalendarAddUserForm(Form):
    """
    Form that lets choose family members from displayed usernames.
    """
    users = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple,
        label='Family members',
        required=False
    )

    def __init__(self, user, family, *args, **kwargs):
        """
        init override that narrows down usernames to user's family usernames. Also excludes logged user.
        :param family:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(family=family).exclude(id=user.id)
