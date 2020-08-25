from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist


def validate_user_exists(value):
    try:
        User.objects.get(username=value)
    except ObjectDoesNotExist:
        raise ValidationError(f'No such user in the database. Please, check for spelling mistakes.')