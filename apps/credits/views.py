from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CreditTransaction, CreditBalance


@login_required
def credit_history(request):
    """View user's credit transaction history"""
    balance, _ = CreditBalance.objects.get_or_create(user=request.user)
    transactions = CreditTransaction.objects.filter(user=request.user)
    
    context = {
        'balance': balance,
        'transactions': transactions,
    }
    
    return render(request, 'credits/history.html', context)
