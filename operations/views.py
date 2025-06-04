import logging
import uuid
from typing import cast

from django.db import transaction
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from organizations.models import Organization, PaymentLogs

from .models import Payment
from .serializers import PaymentSerializer

logger = logging.getLogger(__name__)


class CreatePaymentView(GenericAPIView, mixins.CreateModelMixin):
    """Create операции с Payment"""
    serializer_class = PaymentSerializer

    def post(self, request: Request, *args, **kwargs):
        try:
            operation_id = request.data['operation_id']  # type: ignore
            if payment := Payment.objects.filter(operation_id=operation_id).first():
                serializer = cast(PaymentSerializer, self.get_serializer(payment))
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                    headers=headers
                )

            serializer = cast(PaymentSerializer, self.get_serializer(data=request.data))
            serializer.is_valid(raise_exception=True)

            organization = Organization.objects.select_for_update().get(
                inn=request.data['payer_inn']
            )

            result_serializer = self.perform_create(serializer, organization)
            headers = self.get_success_headers(result_serializer.data)
            return Response(
                result_serializer.data,
                status=status.HTTP_200_OK,
                headers=headers
            )

        except Organization.DoesNotExist:
            logger.error(f"Organization with INN {serializer.validated_data['payer_inn']} not found")  # type: ignore
            return Response(
                {"detail": "Organization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.exception(f"Payment creation failed {e=}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer: PaymentSerializer, organization: Organization):
        with transaction.atomic():
            payment: Payment = serializer.save()

            new_balance = organization.balance + payment.amount
            PaymentLogs.objects.create(
                organization=organization,
                payment=payment,
                amount=payment.amount,
                organization_balance_before=organization.balance,
                organization_balance_after=new_balance
            )

            organization.balance = new_balance
            organization.save(update_fields=['balance'])

        return serializer
