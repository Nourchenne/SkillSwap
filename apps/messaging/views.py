from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from apps.accounts.models import User
from .models import Conversation, Message
from .forms import MessageForm
from apps.exchanges.services import ExchangeService
from apps.core.utils import create_notification


@login_required
def inbox(request):
    """View user's conversations"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants', 'messages')
    
    # Get unread count for each conversation
    for conv in conversations:
        conv.unread_count = conv.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()
        conv.last_message = conv.messages.last()
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """View a specific conversation"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )
    
    # Mark messages as read
    conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        # Block sending if the session (skill offer) has ended
        if conversation.skill_offer and not conversation.skill_offer.is_active:
            from django.contrib import messages as django_messages
            django_messages.error(request, 'This session has ended. You can no longer send messages here.')
            return redirect('messaging:conversation', conversation_id=conversation.id)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Update conversation timestamp
            conversation.save()
            
            return redirect('messaging:conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    other_user = conversation.get_other_user(request.user)
    messages_list = conversation.messages.select_related('sender')
    
    is_locked = bool(conversation.skill_offer and not conversation.skill_offer.is_active)

    context = {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages_list,
        'form': form,
        'is_locked': is_locked,
    }
    
    return render(request, 'messaging/conversation.html', context)


@login_required
def end_course(request, conversation_id):
    """Teacher ends course in a group chat for a skill offer."""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    offer = conversation.skill_offer
    if not offer:
        django_messages.error(request, 'This is not a course group chat.')
        return redirect('messaging:conversation', conversation_id=conversation.id)
    if request.user != offer.user:
        django_messages.error(request, 'Only the teacher can end the course.')
        return redirect('messaging:conversation', conversation_id=conversation.id)

    count = ExchangeService.complete_offer(offer)

    # Notify all participants except teacher
    for participant in conversation.participants.exclude(id=request.user.id):
        create_notification(
            user=participant,
            message=f"Course '{offer.title}' has ended.",
            url=f"/messages/conversation/{conversation.id}/",
            type='message'
        )

    django_messages.success(request, f'Course ended. Completed {count} exchanges.')
    return redirect('messaging:conversation', conversation_id=conversation.id)


@login_required
def start_conversation(request, username):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(User, username=username)
    
    if other_user == request.user:
        django_messages.error(request, "You can't message yourself!")
        return redirect('messaging:inbox')
    
    # Check if conversation already exists
    existing = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=other_user).first()
    
    if existing:
        return redirect('messaging:conversation', conversation_id=existing.id)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    return redirect('messaging:conversation', conversation_id=conversation.id)

