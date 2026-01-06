from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class CreditRequiredMixin(LoginRequiredMixin):
    """Mixin to check if user has enough credits"""
    required_credits = 1
    
    def dispatch(self, request, *args, **kwargs):
        from apps.credits.models import CreditBalance
        
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            balance = CreditBalance.objects.get(user=request.user)
            if balance.balance < self.required_credits:
                messages.error(request, "You don't have enough credits!")
                return redirect('credits:history')
        except CreditBalance.DoesNotExist:
            messages.error(request, "Credit balance not found!")
            return redirect('accounts:dashboard')
        
        return super().dispatch(request, *args, **kwargs)