from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .services import CreditService


@receiver(post_save, sender=User)
def create_credit_balance(sender, instance, created, **kwargs):
    """Create credit balance when user is created"""
    if created:
        CreditService.add_bonus_credits(
            user=instance,
            amount=5,
            description="Welcome bonus"
        )
