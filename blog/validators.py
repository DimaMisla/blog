import re

from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_file_size = 1 * 1024 * 1024
    if file.size > max_file_size:
        raise ValidationError("Max file size must be 1 MB")


def validate_title(title):
    match = re.match(r'^[A-Za-z]+', title)
    if not match:
        raise ValidationError("Title must start with english letter")
