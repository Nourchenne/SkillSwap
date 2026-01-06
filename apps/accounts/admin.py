from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 
                    'location_city', 'id_verified', 'created_at']
    list_filter = ['id_verified', 'email_verified', 'location_city', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'location_city']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('SkillSwap Info', {
            'fields': ('phone_number', 'location_city', 'location_zip', 
                      'latitude', 'longitude', 'id_verified', 'email_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'location_city')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skills_offered_count', 'exchanges_completed', 
                    'available_for_exchange', 'created_at']
    list_filter = ['available_for_exchange', 'email_notifications']
    search_fields = ['user__username', 'user__email', 'bio']
    raw_id_fields = ['user']

