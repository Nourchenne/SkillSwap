from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.skills.models import SkillOffer
from apps.credits.models import CreditBalance
from .models import Exchange
from .forms import ExchangeProposalForm
from .services import ExchangeService


@login_required
def propose_exchange(request, offer_id):
    """Propose an exchange for a skill offer"""
    offer = get_object_or_404(SkillOffer, pk=offer_id, is_active=True)
    
    if request.user == offer.user:
        messages.error(request, "You can't learn from yourself!")
        return redirect('skills:detail', pk=offer_id)
    
    # Check credit balance
    try:
        balance = CreditBalance.objects.get(user=request.user)
        if balance.balance < offer.credits_required:
            messages.error(request, "You don't have enough credits!")
            return redirect('skills:detail', pk=offer_id)
    except CreditBalance.DoesNotExist:
        messages.error(request, "Credit balance not found!")
        return redirect('skills:detail', pk=offer_id)
    
    if request.method == 'POST':
        # Check if already applied
        from apps.skills.models import SkillApplication
        if SkillApplication.objects.filter(user=request.user, skill_offer=offer).exists():
            messages.warning(request, "You have already applied for this skill!")
            return redirect('skills:browse')

        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.skill_offer = offer
            exchange.teacher = offer.user
            exchange.learner = request.user
            exchange.duration_hours = offer.duration_hours
            exchange.credits_amount = offer.credits_required
            exchange.save()
            
            # Create SkillApplication record
            SkillApplication.objects.create(
                user=request.user,
                skill_offer=offer,
                status='pending'
            )

            # Notify teacher about new proposal
            from apps.core.utils import create_notification
            create_notification(
                user=offer.user,
                message=f"New exchange proposal from {request.user.username} for '{offer.title}'",
                url=f"/accounts/dashboard/",
                type='exchange_proposed'
            )
            
            messages.success(request, 'Exchange proposed! Waiting for teacher confirmation.')
            return redirect('accounts:dashboard')
    else:
        form = ExchangeProposalForm(initial={
            'duration_hours': offer.duration_hours
        })
    
    context = {
        'form': form,
        'offer': offer,
    }
    
    return render(request, 'exchanges/propose.html', context)


@login_required
@require_http_methods(["POST"])
def accept_exchange(request, exchange_id):
    """Teacher accepts an exchange proposal"""
    exchange = get_object_or_404(
        Exchange,
        pk=exchange_id,
        teacher=request.user,
        status='proposed'
    )

    # Enforce max group size for the offer
    offer = exchange.skill_offer
    from apps.exchanges.models import Exchange as Ex
    current_group = Ex.objects.filter(
        skill_offer=offer,
        status__in=['accepted', 'scheduled', 'in_progress']
    ).count()
    # current_group counts already accepted learners; accepting one more must not exceed max_group_size
    if current_group >= offer.max_group_size:
        messages.error(request, 'Group is full. You cannot accept more learners for this session.')
        return redirect('accounts:dashboard')
    
    ExchangeService.accept_exchange(exchange)
    messages.success(request, 'Exchange accepted! Coordinate with the learner.')
    return redirect('accounts:dashboard')


@login_required
@require_http_methods(["POST"])
def confirm_completion(request, exchange_id):
    """Both parties confirm exchange completion"""
    exchange = get_object_or_404(
        Exchange,
        pk=exchange_id,
        status__in=['scheduled', 'in_progress', 'accepted']
    )
    
    if request.user == exchange.teacher:
        exchange.teacher_confirmed = True
    elif request.user == exchange.learner:
        exchange.learner_confirmed = True
    else:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    exchange.save()
    
    # If both confirmed, complete the exchange
    if ExchangeService.complete_exchange(exchange):
        messages.success(
            request,
            f'Exchange completed! {exchange.credits_amount} credits transferred.'
        )
    else:
        messages.success(request, 'Confirmation received. Waiting for other party.')
    
    return redirect('accounts:dashboard')

