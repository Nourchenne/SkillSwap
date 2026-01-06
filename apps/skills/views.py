from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Case, When, IntegerField
from .models import SkillOffer, SkillRequest, SkillCategory
from .forms import SkillOfferForm, SkillRequestForm, SkillSearchForm


def browse_skills(request):
    """Browse available skill offers with filters"""
    offers = SkillOffer.objects.filter(is_active=True).select_related(
        'user', 'category'
    )
    
    # Apply filters
    form = SkillSearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        delivery = form.cleaned_data.get('delivery')
        city = form.cleaned_data.get('city')
        
        if search:
            offers = offers.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        if category:
            offers = offers.filter(category__slug=category)
        if delivery:
            offers = offers.filter(
                Q(delivery_method=delivery) | Q(delivery_method='both')
            )
        if city:
            offers = offers.filter(user__location_city__icontains=city)
    
    # Prefer local offers if user has a city, but don't hide other offers
    if request.user.is_authenticated and request.user.location_city:
        offers = offers.annotate(
            city_match=Case(
                When(user__location_city=request.user.location_city, then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-city_match', '-created_at')
    else:
        offers = offers.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(offers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = SkillCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'form': form,
    }
    
    return render(request, 'skills/browse.html', context)


def skill_detail(request, pk):
    """View a specific skill offer"""
    from apps.reviews.models import Review
    from apps.exchanges.models import Exchange
    
    offer = get_object_or_404(
        SkillOffer.objects.select_related('user', 'category'),
        pk=pk
    )
    
    # Increment view count
    offer.view_count += 1
    offer.save(update_fields=['view_count'])
    
    # Get teacher's stats
    teacher_reviews = Review.objects.filter(reviewee=offer.user)
    avg_rating = teacher_reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    completed_count = Exchange.objects.filter(
        teacher=offer.user, 
        status='completed'
    ).count()
    
    # Check if current user can propose exchange
    can_propose = False
    if request.user.is_authenticated and request.user != offer.user:
        from apps.credits.models import CreditBalance
        try:
            balance = CreditBalance.objects.get(user=request.user)
            can_propose = balance.balance >= offer.credits_required
        except CreditBalance.DoesNotExist:
            pass
    
    context = {
        'offer': offer,
        'avg_rating': round(avg_rating, 1),
        'review_count': teacher_reviews.count(),
        'completed_count': completed_count,
        'can_propose': can_propose,
    }
    
    return render(request, 'skills/detail.html', context)


@login_required
def create_skill_offer(request):
    """Create a new skill offer"""
    if request.method == 'POST':
        form = SkillOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            
            # Update user profile
            profile = request.user.profile
            profile.skills_offered_count += 1
            profile.save()
            
            messages.success(request, 'Skill offer created successfully!')
            return redirect('accounts:dashboard')
    else:
        form = SkillOfferForm()
    
    return render(request, 'skills/create_offer.html', {'form': form})


@login_required
def create_skill_request(request):
    """Create a skill learning request"""
    if request.method == 'POST':
        form = SkillRequestForm(request.POST)
        if form.is_valid():
            skill_request = form.save(commit=False)
            skill_request.user = request.user
            skill_request.save()
            messages.success(request, 'Skill request posted!')
            return redirect('accounts:dashboard')
    else:
        form = SkillRequestForm()
    
    return render(request, 'skills/create_request.html', {'form': form})


@login_required
def edit_skill_offer(request, pk):
    """Edit an existing skill offer"""
    offer = get_object_or_404(SkillOffer, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SkillOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill offer updated!')
            return redirect('skills:detail', pk=offer.pk)
    else:
        form = SkillOfferForm(instance=offer)
    
    return render(request, 'skills/edit_offer.html', {'form': form, 'offer': offer})


@login_required
def delete_skill_offer(request, pk):
    """Delete a skill offer"""
    offer = get_object_or_404(SkillOffer, pk=pk, user=request.user)
    
    if request.method == 'POST':
        offer.is_active = False
        offer.save()
        messages.success(request, 'Skill offer removed!')
        return redirect('accounts:dashboard')
    
    return render(request, 'skills/delete_offer.html', {'offer': offer})

