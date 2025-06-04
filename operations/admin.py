from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'document_date', 'amount',
                    'payer_inn', 'operation_id', 'created_at', 'updated_at')
    list_filter = ('document_date', 'amount')
    search_fields = ('document_number', 'payer_inn', 'operation_id')
    date_hierarchy = 'document_date'
    ordering = ['-document_date']
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
