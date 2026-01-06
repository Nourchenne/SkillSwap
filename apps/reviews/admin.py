from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'rating', 'skill_quality',
                    'communication', 'reliability', 'is_visible', 'created_at']
    list_filter = ['rating', 'is_flagged', 'is_visible', 'created_at']
    search_fields = ['reviewer__username', 'reviewee__username', 'comment']
    raw_id_fields = ['exchange', 'reviewer', 'reviewee']
    
    actions = ['flag_reviews', 'unflag_reviews', 'hide_reviews', 'show_reviews']
    
    def flag_reviews(self, request, queryset):
        queryset.update(is_flagged=True)
    flag_reviews.short_description = "Flag selected reviews"
    
    def unflag_reviews(self, request, queryset):
        queryset.update(is_flagged=False)
    unflag_reviews.short_description = "Unflag selected reviews"
    
    def hide_reviews(self, request, queryset):
        queryset.update(is_visible=False)
    hide_reviews.short_description = "Hide selected reviews"
    
    def show_reviews(self, request, queryset):
        queryset.update(is_visible=True)
    show_reviews.short_description = "Show selected reviews"

