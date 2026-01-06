from django.contrib import admin
from .models import CreditBalance, CreditTransaction


@admin.register(CreditBalance)
class CreditBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'total_earned', 'total_spent', 'updated_at']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 
                    'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user', 'exchange']
    readonly_fields = ['created_at']
