from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.skills.models import SkillOffer
from apps.messaging.models import Conversation


@receiver(post_save, sender=SkillOffer)
def create_group_conversation_for_offer(sender, instance: SkillOffer, created: bool, **kwargs):
    """Auto-create a group conversation for a new skill offer.

    Ensures there's exactly one conversation associated with the offer and
    the teacher is a participant by default. Learners are added upon acceptance.
    """
    if not created:
        return

    # If a conversation already exists (e.g., data migration), don't duplicate
    convo = Conversation.objects.filter(skill_offer=instance).first()
    if convo is None:
        convo = Conversation.objects.create(skill_offer=instance)
    # Ensure the teacher is in the conversation participants
    if instance.user and instance.user not in convo.participants.all():
        convo.participants.add(instance.user)
