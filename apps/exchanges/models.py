from django.db import models
from django.conf import settings
from django.utils import timezone


class Exchange(models.Model):
    """Represents a skill exchange transaction"""
    STATUS_CHOICES = [
        ('proposed', 'Proposed'),
        ('accepted', 'Accepted'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ]
    
    skill_offer = models.ForeignKey(
        'skills.SkillOffer',
        on_delete=models.CASCADE,
        related_name='exchanges'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exchanges_as_teacher'
    )
    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exchanges_as_learner'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='proposed'
    )
    
    # Session details
    scheduled_datetime = models.DateTimeField(null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=3, decimal_places=1)
    credits_amount = models.IntegerField()
    
    location_details = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Confirmation
    teacher_confirmed = models.BooleanField(default=False)
    learner_confirmed = models.BooleanField(default=False)
    
    # Timestamps
    proposed_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'exchanges'
        ordering = ['-proposed_at']
        indexes = [
            models.Index(fields=['teacher', 'status']),
            models.Index(fields=['learner', 'status']),
        ]
    
    def __str__(self):
        return f"{self.skill_offer.title}: {self.teacher.username} → {self.learner.username}"
