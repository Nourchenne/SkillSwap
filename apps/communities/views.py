from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Community, CommunityMembership


def community_list(request):
    """List all communities"""
    communities = Community.objects.filter(is_active=True, is_public=True)
    
    # Filter by city if provided
    city = request.GET.get('city')
    if city:
        communities = communities.filter(city__icontains=city)
    
    context = {
        'communities': communities,
    }
    
    return render(request, 'communities/list.html', context)


def community_detail(request, slug):
    """View a specific community"""
    community = get_object_or_404(Community, slug=slug, is_active=True)
    
    is_member = False
    if request.user.is_authenticated:
        is_member = CommunityMembership.objects.filter(
            user=request.user,
            community=community
        ).exists()
    
    # Get recent members
    recent_members = community.members.all()[:12]
    
    context = {
        'community': community,
        'is_member': is_member,
        'recent_members': recent_members,
    }
    
    return render(request, 'communities/detail.html', context)


@login_required
def join_community(request, slug):
    """Join a community"""
    community = get_object_or_404(Community, slug=slug, is_active=True)
    
    membership, created = CommunityMembership.objects.get_or_create(
        user=request.user,
        community=community
    )
    
    if created:
        messages.success(request, f'You joined {community.name}!')
    else:
        messages.info(request, 'You are already a member')
    
    return redirect('communities:detail', slug=slug)


@login_required
def leave_community(request, slug):
    """Leave a community"""
    community = get_object_or_404(Community, slug=slug)
    
    CommunityMembership.objects.filter(
        user=request.user,
        community=community
    ).delete()
    
    messages.success(request, f'You left {community.name}')
    return redirect('communities:list')

