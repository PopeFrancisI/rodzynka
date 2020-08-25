from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from family.models import Family


def validate_user_exists(value):
    try:
        User.objects.get(username=value)
    except ObjectDoesNotExist:
        raise ValidationError(f'No such user in the database. Please, check for spelling mistakes.')


def validate_family_exists(value):
    try:
        Family.objects.get(name=value)
    except ObjectDoesNotExist:
        raise ValidationError(f'No such family in the database. Please, check for spelling mistakes.')
