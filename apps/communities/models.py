from django.db import models
from django.conf import settings


class Community(models.Model):
    """Local community hubs"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    city = models.CharField(max_length=100)
    
    # Membership
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommunityMembership',
        related_name='communities'
    )
    
    # Settings
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'communities'
        verbose_name_plural = "Communities"
        ordering = ['city', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.city})"
    
    @property
    def member_count(self):
        return self.members.count()


class CommunityMembership(models.Model):
    """Membership relationship between users and communities"""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'community_memberships'
        unique_together = ['user', 'community']
    
    def __str__(self):
        return f"{self.user.username} in {self.community.name}"

