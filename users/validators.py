from django.core.exceptions import ValidationError, ObjectDoesNotExist

from family.models import Family


def validate_name_length(value):
    if len(value) < 2 or len(value) > 150:
        raise ValidationError(f'Typed value is too short or too long!')


def validate_name_letters_only(value):
    if not value.isalpha():
        raise ValidationError(f'Typed value contains non-letter characters!')


def validate_family_exists(value):
    try:
        Family.objects.get(name=value)
    except ObjectDoesNotExist:
        raise ValidationError(f'No such family in the database. Please, check for spelling mistakes.')
