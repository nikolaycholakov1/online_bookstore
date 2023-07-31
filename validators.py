from django.core.exceptions import ValidationError


def validate_letters_only(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError('Name can only contain letters and whitespace.')
