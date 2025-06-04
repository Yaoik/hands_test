from rest_framework import serializers

from organizations.models import Organization

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payer_inn = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        pk_field=serializers.CharField()
    )

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
