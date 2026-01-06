from typing import Dict
from django.http import HttpRequest


def notifications(request: HttpRequest) -> Dict[str, int]:
    """Add unread notifications count to template context for authenticated users."""
    try:
        if request.user.is_authenticated:
            from apps.core.models import Notification
            count = Notification.objects.filter(user=request.user, is_read=False).count()
            return {"notifications_count": count}
    except Exception:
        # Fail silently in templates; don't break pages if DB isn't ready
        pass
    return {"notifications_count": 0}
