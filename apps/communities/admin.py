from django.contrib import admin
from .models import Community, CommunityMembership


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'member_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_public', 'city']
    search_fields = ['name', 'city', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['members']


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__username', 'community__name']
    raw_id_fields = ['user', 'community']