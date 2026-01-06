from django.db import transaction
from .models import CreditBalance, CreditTransaction


class CreditService:
    """Business logic for credit operations"""
    
    @staticmethod
    @transaction.atomic
    def transfer_credits(from_user, to_user, amount, exchange=None, reason='exchange'):
        """Transfer credits from one user to another"""
        # Get or create balances
        from_balance, _ = CreditBalance.objects.get_or_create(user=from_user)
        to_balance, _ = CreditBalance.objects.get_or_create(user=to_user)
        
        # Check sufficient balance
        if from_balance.balance < amount:
            raise ValueError("Insufficient credits")
        
        # Update balances
        from_balance.balance -= amount
        from_balance.total_spent += amount
        from_balance.save()
        
        to_balance.balance += amount
        to_balance.total_earned += amount
        to_balance.save()
        
        # Create transactions
        CreditTransaction.objects.create(
            user=from_user,
            exchange=exchange,
            amount=-amount,
            transaction_type=reason,
            balance_after=from_balance.balance,
            description=f"Payment to {to_user.username}"
        )
        
        CreditTransaction.objects.create(
            user=to_user,
            exchange=exchange,
            amount=amount,
            transaction_type=reason,
            balance_after=to_balance.balance,
            description=f"Payment from {from_user.username}"
        )
        
        return from_balance, to_balance
    
    @staticmethod
    @transaction.atomic
    def add_bonus_credits(user, amount, description="Bonus credits"):
        """Add bonus credits to a user"""
        balance, _ = CreditBalance.objects.get_or_create(user=user)
        balance.balance += amount
        balance.total_earned += amount
        balance.save()
        
        CreditTransaction.objects.create(
            user=user,
            amount=amount,
            transaction_type='bonus',
            balance_after=balance.balance,
            description=description
        )
        
        return balance
    
    @staticmethod
    @transaction.atomic
    def refund_credits(user, amount, exchange=None):
        """Refund credits to a user"""
        balance, _ = CreditBalance.objects.get_or_create(user=user)
        balance.balance += amount
        balance.save()
        
        CreditTransaction.objects.create(
            user=user,
            exchange=exchange,
            amount=amount,
            transaction_type='refund',
            balance_after=balance.balance,
            description="Refund for cancelled exchange"
        )
        
        return balance

