from django.core.exceptions import ValidationError


def validate_name_length(value):
    if len(value) < 2 or len(value) > 150:
        raise ValidationError(f'Typed value is too short or too long!')


def validate_name_letters_only(value):
    if not value.isalpha():
        raise ValidationError(f'Typed value contains non-letter characters!')
