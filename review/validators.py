from django.core.exceptions import ValidationError


def validate_rating(value):
    if not (0 <= value <= 5):
        raise ValidationError("Rating must be a floating-point number between 0 and 5.")
