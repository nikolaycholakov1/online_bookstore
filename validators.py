from django.core.exceptions import ValidationError


def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError('Name can only contain letters.')
