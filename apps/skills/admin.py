from django.contrib import admin
from .models import SkillCategory, SkillOffer


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(SkillOffer)
class SkillOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'delivery_method', 
                    'skill_level', 'is_active', 'view_count', 'created_at']
    list_filter = ['is_active', 'category', 'delivery_method', 'skill_level', 'session_type']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user']
    
    actions = ['activate_offers', 'deactivate_offers']
    
    def activate_offers(self, request, queryset):
        queryset.update(is_active=True)
    activate_offers.short_description = "Activate selected offers"
    
    def deactivate_offers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_offers.short_description = "Deactivate selected offers"


# SkillRequest admin removed to keep admin clean and focused on active features.