import logging
from typing import cast
from uuid import UUID

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from operations.models import Payment
from operations.serializers import PaymentSerializer
from operations.tests.factories import PaymentFactory
from organizations.models import Organization, PaymentLogs
from organizations.tests.factories import OrganizationFactory

logger = logging.getLogger(__name__)


@pytest.fixture
def organization() -> Organization:
    return OrganizationFactory(balance=0)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreatePaymentView:
    def test_create_payment_success(
        self, api_client: APIClient, organization: Organization
    ) -> None:
        payment_data = {
            "operation_id": str(UUID(int=0)),
            "amount": 1000,
            "payer_inn": organization.inn,
            "document_number": "PAY-12345",
            "document_date": "2025-06-01T12:00:00Z",
        }
        url = reverse("payment:create-payment-webhook")
        response = cast(Response, api_client.post(url, payment_data, format="json"))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["operation_id"] == payment_data["operation_id"]  # type: ignore
        assert response.data["amount"] == payment_data["amount"]  # type: ignore
        assert response.data["payer_inn"] == organization.inn  # type: ignore
        assert response.data["document_number"] == payment_data["document_number"]  # type: ignore

        payment = Payment.objects.get(operation_id=payment_data["operation_id"])
        organization.refresh_from_db()
        assert payment.amount == 1000
        assert payment.payer_inn == organization.inn

        payment_log = PaymentLogs.objects.get(payment=payment)
        assert payment_log.organization == organization
        assert payment_log.amount == 1000
        assert payment_log.organization_balance_before == organization.balance - 1000
        assert payment_log.organization_balance_after == organization.balance
        assert organization.balance == payment_log.organization_balance_after

    def test_create_payment_duplicate_operation_id(
        self, api_client: APIClient, organization: Organization
    ) -> None:
        payment = PaymentFactory(payer_inn=organization.inn)
        payment_data = {
            "operation_id": str(payment.operation_id),
            "amount": 1000,
            "payer_inn": organization.inn,
            "document_number": "PAY-12345",
            "document_date": "2025-06-01T12:00:00Z",
        }
        url = reverse("payment:create-payment-webhook")
        response = cast(Response, api_client.post(url, payment_data, format="json"))
        logger.info(f'{payment_data=}')
        logger.info(f'{response=}')
        logger.info(f'{response.data=}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data["operation_id"] == str(payment.operation_id)  # type: ignore
        assert Payment.objects.filter(operation_id=payment.operation_id).count() == 1
        assert PaymentLogs.objects.filter(payment=payment).count() == 0

    def test_create_payment_non_existent_organization(
        self, api_client: APIClient
    ) -> None:
        payment_data = {
            "operation_id": str(UUID(int=0)),
            "amount": 1000,
            "payer_inn": "123456789012",
            "document_number": "PAY-12345",
            "document_date": "2025-06-01T12:00:00Z",
        }
        url = reverse("payment:create-payment-webhook")
        response = cast(Response, api_client.post(url, payment_data, format="json"))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Organization not found" in str(response.data)
        assert not Payment.objects.filter(operation_id=payment_data["operation_id"]).exists()

    def test_create_payment_invalid_operation_id(
        self, api_client: APIClient, organization: Organization
    ) -> None:
        payment_data = {
            "operation_id": "invalid-uuid",
            "amount": 1000,
            "payer_inn": organization.inn,
            "document_number": "PAY-12345",
            "document_date": "2025-06-01T12:00:00Z",
        }
        url = reverse("payment:create-payment-webhook")
        response = cast(Response, api_client.post(url, payment_data, format="json"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "invalid" in str(response.data)
        assert not Payment.objects.filter(payer_inn=organization.inn).exists()

    def test_create_payment_missing_required_field(
        self, api_client: APIClient, organization: Organization
    ) -> None:
        payment_data = {
            "operation_id": str(UUID(int=0)),
            "payer_inn": organization.inn,
            "document_number": "PAY-12345",
            "document_date": "2025-06-01T12:00:00Z",
        }
        url = reverse("payment:create-payment-webhook")
        response = cast(Response, api_client.post(url, payment_data, format="json"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data['detail']  # type: ignore
        assert not Payment.objects.filter(payer_inn=organization.inn).exists()
