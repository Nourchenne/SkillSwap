from django.db import models
from django.conf import settings


class CreditBalance(models.Model):
    """Track user's time credit balance"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credit_balance'
    )
    balance = models.IntegerField(default=5)  # Starting credits
    total_earned = models.IntegerField(default=0)
    total_spent = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'credit_balances'
    
    def __str__(self):
        return f"{self.user.username}: {self.balance} credits"


class CreditTransaction(models.Model):
    """Track all time credit movements"""
    TRANSACTION_TYPES = [
        ('exchange', 'Skill Exchange'),
        ('bonus', 'Welcome Bonus'),
        ('admin_adjustment', 'Admin Adjustment'),
        ('refund', 'Refund'),
        ('referral', 'Referral Bonus'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credit_transactions'
    )
    exchange = models.ForeignKey(
        'exchanges.Exchange',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    amount = models.IntegerField()  # Positive for credit, negative for debit
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    balance_after = models.IntegerField()
    
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'credit_transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.amount:+d} credits"