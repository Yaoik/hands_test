import uuid

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'operation_id',
            'amount',
            'payer_inn',
            'document_number',
            'document_date',
        )
        read_only_fields = (
            'created_at',
            'updated_at',
        )
