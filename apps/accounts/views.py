from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from .models import User, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the user in
            login(request, user)
            
            # Welcome message
            messages.success(request, f'Welcome to SkillSwap, {user.first_name}! You have 5 free credits to start.')
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard showing their activity"""
    from apps.skills.models import SkillOffer
    from apps.exchanges.models import Exchange
    from apps.reviews.models import Review
    from apps.credits.models import CreditBalance
    
    user = request.user
    
    # Get user's credit balance
    try:
        credit_balance = CreditBalance.objects.get(user=user)
    except CreditBalance.DoesNotExist:
        credit_balance = CreditBalance.objects.create(user=user)
    
    # Get user's active skill offers
    my_offers = SkillOffer.objects.filter(user=user, is_active=True)
    
    # Exchanges
    pending_as_teacher = Exchange.objects.filter(
        teacher=user, 
        status__in=['proposed', 'accepted', 'scheduled']
    ).select_related('learner', 'skill_offer')
    
    pending_as_learner = Exchange.objects.filter(
        learner=user,
        status__in=['proposed', 'accepted', 'scheduled']
    ).select_related('teacher', 'skill_offer')
    
    completed_exchanges = Exchange.objects.filter(
        Q(teacher=user) | Q(learner=user),
        status='completed'
    ).count()
    
    # Notifications
    from apps.core.models import Notification
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]
    
    # Reviews
    reviews = Review.objects.filter(reviewee=user).select_related('reviewer')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    # Available offers the user could join (not mine, active, optionally same city, affordable)
    available_offers = SkillOffer.objects.filter(is_active=True).exclude(user=user).select_related('user', 'category')
    if user.location_city:
        available_offers = available_offers.filter(user__location_city=user.location_city)
    if credit_balance.balance is not None:
        # credits_required ~= int(duration_hours); filter by duration_hours <= balance
        available_offers = available_offers.filter(duration_hours__lte=credit_balance.balance)
    available_offers = available_offers.order_by('-view_count', '-created_at')[:6]
    
    context = {
        'my_offers': my_offers,
        'pending_as_teacher': pending_as_teacher,
        'pending_as_learner': pending_as_learner,
        'completed_exchanges': completed_exchanges,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': reviews.count(),
        'credit_balance': credit_balance.balance,
        'notifications': notifications,
        'available_offers': available_offers,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request, username):
    """View user profile"""
    from apps.skills.models import SkillOffer
    from apps.exchanges.models import Exchange
    from apps.reviews.models import Review
    
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    
    offers = SkillOffer.objects.filter(user=profile_user, is_active=True)
    reviews = Review.objects.filter(reviewee=profile_user).select_related('reviewer', 'exchange')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    completed_as_teacher = Exchange.objects.filter(
        teacher=profile_user,
        status='completed'
    ).count()
    
    completed_as_learner = Exchange.objects.filter(
        learner=profile_user,
        status='completed'
    ).count()
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'offers': offers,
        'reviews': reviews[:5],  # Show latest 5
        'avg_rating': round(avg_rating, 1),
        'completed_as_teacher': completed_as_teacher,
        'completed_as_learner': completed_as_learner,
        'is_own_profile': request.user == profile_user,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'accounts/edit_profile.html', context)
