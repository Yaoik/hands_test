from django.contrib import admin

from .models import Organization, PaymentLogs


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('inn', 'balance', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('inn',)
    ordering = ['inn']
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(PaymentLogs)
class PaymentLogsAdmin(admin.ModelAdmin):
    list_display = ('payment', 'organization', 'amount', 'organization_balance_before',
                    'organization_balance_after', 'created_at', 'updated_at')
    list_filter = ('organization', 'created_at')
    search_fields = ('payment__document_number', 'organization__inn')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = list_display

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('organization', 'payment')
