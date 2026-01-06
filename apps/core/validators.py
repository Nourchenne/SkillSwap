from django.core.exceptions import ValidationError
import re


def validate_username_format(value):
    """Validate username format"""
    if not re.match(r'^[\w.-]+$', value):
        raise ValidationError(
            'Username can only contain letters, numbers, dots, and hyphens'
        )


def validate_positive_credits(value):
    """Validate credit amount is positive"""
    if value <= 0:
        raise ValidationError('Credit amount must be positive')
