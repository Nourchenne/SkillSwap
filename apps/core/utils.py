from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification


def send_notification_email(user, subject, template_name, context):
    """Send notification email to user"""
    if not user.profile.email_notifications:
        return
    
    html_message = render_to_string(template_name, context)
    
    send_mail(
        subject=subject,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,
    )


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance


def create_notification(user, message, url='', type='message'):
    """Create and store an in-app notification"""
    try:
        Notification.objects.create(user=user, message=message, url=url, type=type)
    except Exception:
        # Avoid breaking the main flow if notifications fail
        pass
