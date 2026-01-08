from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.urls import reverse


class SkillCategory(models.Model):
    """Categories for organizing skills"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True, help_text="Dynamic logo URL for the category")
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'skill_categories'
        verbose_name_plural = "Skill Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('skills:browse') + f'?category={self.slug}'


class SkillOffer(models.Model):
    """Skills that users can teach/offer"""
    DELIVERY_CHOICES = [
        ('in_person', 'In-Person'),
        ('video_call', 'Video Call'),
        ('both', 'Both'),
    ]
    
    SESSION_TYPES = [
        ('one_on_one', '1-on-1 Session'),
        ('small_group', 'Small Group (2-5)'),
        ('workshop', 'Workshop (6+)'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill_offers'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='skills'
    )
    
    # Session details
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default='both'
    )
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPES,
        default='one_on_one'
    )
    max_group_size = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    duration_hours = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=1.0,
        validators=[MinValueValidator(0.5)]
    )
    
    # Additional info
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('all', 'All Levels'),
        ],
        default='all'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'skill_offers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('skills:detail', kwargs={'pk': self.pk})
    
    @property
    def credits_required(self):
        """Calculate credits required based on duration"""
        return int(self.duration_hours)


class SkillRequest(models.Model):
    """Skills that users want to learn"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill_requests'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requests'
    )
    
    # Preferences
    preferred_delivery = models.CharField(
        max_length=20,
        choices=SkillOffer.DELIVERY_CHOICES,
        default='both'
    )
    urgency = models.CharField(
        max_length=20,
        choices=[
            ('flexible', 'Flexible'),
            ('soon', 'Within a month'),
            ('urgent', 'ASAP'),
        ],
        default='flexible'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    is_fulfilled = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'skill_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class SkillApplication(models.Model):
    """Tracks users applying for a specific skill offer"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill_applications'
    )
    skill_offer = models.ForeignKey(
        SkillOffer,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skill_applications'
        unique_together = ('user', 'skill_offer')
        verbose_name = "Skill Application"
        verbose_name_plural = "Skill Applications"

    def __str__(self):
        return f"{self.user.username} applied for {self.skill_offer.title}"
