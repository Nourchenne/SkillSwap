from typing import Optional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse

from .models import Notification
from django.db.models import Avg, Count, Q, F, ExpressionWrapper


def home(request: HttpRequest) -> HttpResponse:
    """Home page with featured skill offers and search CTA."""
    from apps.skills.models import SkillOffer
    # Featured: active offers with rating and capacity info
    featured_offers = SkillOffer.objects.filter(is_active=True).select_related(
        'user', 'category'
    ).annotate(
        avg_rating=Avg('user__reviews_received__rating'),
        review_count=Count('user__reviews_received'),
        active_count=Count(
            'exchanges',
            filter=Q(exchanges__status__in=['accepted', 'scheduled', 'in_progress'])
        ),
        spots_left=ExpressionWrapper(
            F('max_group_size') - Count(
                'exchanges',
                filter=Q(exchanges__status__in=['accepted', 'scheduled', 'in_progress'])
            ),
            output_field=Count('pk').output_field
        ),
    ).order_by('-view_count', '-created_at')[:8]

    # User balance to decide CTA state
    user_balance = None
    if request.user.is_authenticated:
        try:
            from apps.credits.models import CreditBalance
            bal_obj = CreditBalance.objects.get(user=request.user)
            user_balance = bal_obj.balance
        except Exception:
            user_balance = None

    return render(request, 'home.html', {
        'featured_offers': featured_offers,
        'user_balance': user_balance,
    })


@login_required
def notifications_list(request: HttpRequest) -> HttpResponse:
    """List a user's notifications with actions to mark read/unread."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'core/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def mark_notification_read(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        messages.success(request, 'Notification marked as read.')
    return redirect(_next_url(request))


@login_required
def mark_notification_unread(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = False
        notification.save(update_fields=['is_read'])
        messages.success(request, 'Notification marked as unread.')
    return redirect(_next_url(request))


@login_required
def mark_all_notifications_read(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        if count:
            messages.success(request, f'Marked {count} notifications as read.')
        else:
            messages.info(request, 'No unread notifications.')
    return redirect(_next_url(request))


def _next_url(request: HttpRequest) -> str:
    """Get redirect target from ?next= or fallback to notifications list."""
    next_url: Optional[str] = request.GET.get('next')
    return next_url or reverse('core:notifications')


# --- JSON API for navbar dropdown ---

@login_required
def api_notifications_list(request: HttpRequest) -> JsonResponse:
    """Return latest notifications for the dropdown (unread first)."""
    from django.contrib.humanize.templatetags.humanize import naturaltime
    qs = Notification.objects.filter(user=request.user).order_by('is_read', '-created_at')[:10]
    items = [
        {
            'id': n.id,
            'type': n.type,
            'message': n.message,
            'url': n.url,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
            'created_at_human': naturaltime(n.created_at),
        }
        for n in qs
    ]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'status': 'success', 'notifications': items, 'unread_count': unread_count})


@login_required
def api_unread_count(request: HttpRequest) -> JsonResponse:
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})


@login_required
def api_mark_read(request: HttpRequest, pk: int) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'ok': True, 'unread_count': count})


@login_required
def api_mark_all_read(request: HttpRequest) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    updated = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'ok': True, 'updated': updated, 'unread_count': count})
from django.shortcuts import render

@login_required
def leaderboard(request):
    """Show top performers with podium and full ranking table."""
    from apps.accounts.models import UserProfile
    from apps.credits.models import CreditBalance
    from apps.reviews.models import Review
    from django.contrib.auth import get_user_model
    from django.db.models import Avg, Count, Sum
    
    User = get_user_model()
    
    # Enrich users with everything we need:
    # 1. Total earned credits (the primary score)
    # 2. Exchanges completed (from profile)
    # 3. Badge count
    # 4. Average rating
    
    performers = User.objects.annotate(
        earned_credits=Sum('credit_balance__total_earned'),
        badge_count=Count('badges', distinct=True),
        avg_rating=Avg('reviews_received__rating'),
        completed_count=Count('exchanges_as_teacher', filter=Q(exchanges_as_teacher__status='completed'), distinct=True)
    ).order_by('-earned_credits', '-completed_count', '-badge_count')[:50]
    
    # Extract top 3 for the podium
    top_3 = performers[:3]
    # The rest for the table
    remaining = performers[3:]
    
    return render(request, 'core/leaderboard.html', {
        'top_3': top_3,
        'remaining': remaining,
        'current_user_id': request.user.id
    })
