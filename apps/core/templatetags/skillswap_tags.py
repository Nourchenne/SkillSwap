from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def stars(rating):
    """Convert rating to star display"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    html = '★' * full_stars
    if half_star:
        html += '☆'
    html += '☆' * empty_stars
    
    return mark_safe(html)


@register.filter
def credit_format(amount):
    """Format credit amount with sign"""
    if amount > 0:
        return f"+{amount}"
    return str(amount)


@register.simple_tag
def user_initials(user):
    """Get user initials"""
    if user.first_name and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    return user.username[0].upper()


@register.filter(name='add_class')
def add_class(value, css_class):
    """Add a CSS class to a form field widget"""
    return value.as_widget(attrs={'class': css_class})


@register.filter(name='is_checkbox')
def is_checkbox(field):
    """Check if a field's widget is a checkbox"""
    return field.field.widget.__class__.__name__ == 'CheckboxInput'


@register.filter(name='is_radio')
def is_radio(field):
    """Check if a field's widget is a radio select"""
    return field.field.widget.__class__.__name__ == 'RadioSelect'