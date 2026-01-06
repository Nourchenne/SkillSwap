from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Conversation between two users"""
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    # Group chat for a skill offer (teacher + accepted learners)
    skill_offer = models.ForeignKey(
        'skills.SkillOffer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='group_conversation'
    )
    exchange = models.ForeignKey(
        'exchanges.Exchange',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.skill_offer:
            return f"Group Chat: {self.skill_offer.title}"
        usernames = [u.username for u in self.participants.all()[:2]]
        return f"Conversation: {' & '.join(usernames)}"
    
    def get_other_user(self, user):
        """Get the other participant in the conversation"""
        return self.participants.exclude(id=user.id).first()


class Message(models.Model):
    """Direct messages between users"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_sent'
    )
    
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"