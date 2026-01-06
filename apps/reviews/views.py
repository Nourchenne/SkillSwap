from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.exchanges.models import Exchange
from .models import Review
from .forms import ReviewForm


@login_required
def leave_review(request, exchange_id):
    """Leave a review after completing an exchange"""
    exchange = get_object_or_404(
        Exchange,
        pk=exchange_id,
        status='completed'
    )
    
    # Determine who is being reviewed
    if request.user == exchange.learner:
        reviewee = exchange.teacher
    elif request.user == exchange.teacher:
        reviewee = exchange.learner
    else:
        messages.error(request, 'Not authorized')
        return redirect('accounts:dashboard')
    
    # Check if review already exists
    if Review.objects.filter(exchange=exchange, reviewer=request.user).exists():
        messages.info(request, 'You already reviewed this exchange')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.exchange = exchange
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, 'Review submitted!')
            return redirect('accounts:dashboard')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'exchange': exchange,
        'reviewee': reviewee,
    }
    
    return render(request, 'reviews/create.html', context)

