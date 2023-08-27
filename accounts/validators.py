import re
from datetime import date

from django.core.exceptions import ValidationError


def validate_username(username: str) -> None:
    if re.search(r'^[A-Za-z_]*$', username) is None:
        raise ValidationError(f'{username} contains non-english letters or characters other than underscore')
    if username.startswith("_") or username.endswith("_"):
        raise ValidationError(f'{username} cannot start or end with an underscore')


def validate_name(name: str):
    if re.search(r'^[A-Za-z]*$', name) is None:
        raise ValidationError(f'{name} contains non-english letters')


def validate_password_strength(value: str) -> None:
    if len(value) < 8:
        raise ValidationError("Password must contain at least 8 characters.")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', value):
        raise ValidationError("Password must contain at least one lower letter.")
    if not re.search(r'\d', value):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[@$!%*?&#]', value):
        raise ValidationError("Password must contain at least one special character: @, $, !, %, *, ?, #, &.")


def validate_birth_date(birth_date):
    if birth_date.year < 1900:
        raise ValidationError('Invalid birth date - year must be greater than 1900.')

    age = (date.today() - birth_date).days // 365
    if age < 18:
        raise ValidationError('You must be at least 18 years old to register.')
