from django.utils import timezone
from django.db import transaction
from apps.credits.services import CreditService
from apps.messaging.models import Conversation
from apps.core.utils import create_notification


class ExchangeService:
    """Business logic for exchange operations"""
    
    @staticmethod
    @transaction.atomic
    def accept_exchange(exchange):
        """Teacher accepts exchange proposal"""
        exchange.status = 'accepted'
        exchange.accepted_at = timezone.now()
        exchange.save()
        # Create or fetch a group conversation linked to the skill offer
        convo = Conversation.objects.filter(skill_offer=exchange.skill_offer).first()
        if not convo:
            convo = Conversation.objects.create(skill_offer=exchange.skill_offer)
            convo.participants.add(exchange.teacher)
        # Add learner to group chat
        convo.participants.add(exchange.learner)
        
        # Notify learner
        create_notification(
            user=exchange.learner,
            message=f"Your proposal for '{exchange.skill_offer.title}' was accepted",
            url=f"/messages/conversation/{convo.id}/",
            type='exchange_accepted'
        )
        return exchange
    
    @staticmethod
    @transaction.atomic
    def complete_exchange(exchange):
        """Process exchange completion and credit transfer"""
        if exchange.teacher_confirmed and exchange.learner_confirmed:
            if exchange.status != 'completed':
                # Transfer credits
                CreditService.transfer_credits(
                    from_user=exchange.learner,
                    to_user=exchange.teacher,
                    amount=exchange.credits_amount,
                    exchange=exchange,
                    reason='exchange'
                )
                
                # Update exchange
                exchange.status = 'completed'
                exchange.completed_at = timezone.now()
                exchange.save()
                
                # Update user profiles
                exchange.teacher.profile.exchanges_completed += 1
                exchange.teacher.profile.save()
                
                exchange.learner.profile.exchanges_completed += 1
                exchange.learner.profile.save()
                
            return True
        return False

    @staticmethod
    @transaction.atomic
    def complete_offer(skill_offer):
        """Teacher ends the course for a skill offer; complete all active exchanges."""
        from apps.exchanges.models import Exchange
        active_statuses = ['accepted', 'scheduled', 'in_progress']
        exchanges = Exchange.objects.select_for_update().filter(
            skill_offer=skill_offer,
            status__in=active_statuses
        )
        for ex in exchanges:
            # Avoid double completion
            if ex.status == 'completed':
                continue
            # Transfer credits
            CreditService.transfer_credits(
                from_user=ex.learner,
                to_user=ex.teacher,
                amount=ex.credits_amount,
                exchange=ex,
                reason='exchange'
            )
            ex.status = 'completed'
            ex.completed_at = timezone.now()
            ex.save()
            # Invite learner to review
            create_notification(
                user=ex.learner,
                message=f"Course '{skill_offer.title}' completed. Please leave a review.",
                url=f"/reviews/create/?exchange={ex.id}",
                type='message'
            )
        # After completing exchanges, mark the offer inactive so it is no longer public
        if skill_offer.is_active:
            skill_offer.is_active = False
            skill_offer.save(update_fields=['is_active'])

        return exchanges.count()
        
        # Set offer inactive (no longer publicly listed)
        
    
    @staticmethod
    @transaction.atomic
    def cancel_exchange(exchange, cancelled_by):
        """Cancel an exchange"""
        # Store original status before modifying
        original_status = exchange.status

        exchange.status = 'cancelled'
        exchange.save()

        # If learner paid upfront, refund
        if original_status in ['accepted', 'scheduled']:
            CreditService.refund_credits(
                user=exchange.learner,
                amount=exchange.credits_amount,
                exchange=exchange
            )
