from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.exchanges.models import Exchange
from .models import Badge, UserBadge

@receiver(post_save, sender=Exchange)
def check_first_swap_badge(sender, instance, created, **kwargs):
    """
    Award 'First Swap' badge when an exchange status becomes 'completed'.
    """
    if instance.status == 'completed':
        # Award to learner
        _award_badge(instance.learner, 'first-swap')
        # Award to teacher
        _award_badge(instance.teacher, 'first-swap')

        # Check for 'Power Teacher' (e.g. 5 completed exchanges)
        if instance.teacher.exchanges_as_teacher.filter(status='completed').count() >= 5:
            _award_badge(instance.teacher, 'power-teacher')

def _award_badge(user, badge_slug):
    try:
        badge = Badge.objects.get(slug=badge_slug)
        # get_or_create to avoid duplicates
        UserBadge.objects.get_or_create(user=user, badge=badge)
    except Badge.DoesNotExist:
        pass # Badge not defined in DB yet
