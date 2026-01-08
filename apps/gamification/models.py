from django.db import models
from django.conf import settings

class Badge(models.Model):
    slug = models.SlugField(unique=True, help_text="Unique identifier for the badge logic (e.g. 'first-swap')")
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or Icon class")
    criteria_description = models.CharField(max_length=255, help_text="Short text explaining how to earn it")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-awarded_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
