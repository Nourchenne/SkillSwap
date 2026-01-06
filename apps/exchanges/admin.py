from django.contrib import admin
from .models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'skill_offer', 'teacher', 'learner', 
                    'status', 'credits_amount', 'proposed_at']
    list_filter = ['status', 'proposed_at', 'completed_at']
    search_fields = ['teacher__username', 'learner__username', 
                     'skill_offer__title']
    date_hierarchy = 'proposed_at'
    raw_id_fields = ['skill_offer', 'teacher', 'learner']

