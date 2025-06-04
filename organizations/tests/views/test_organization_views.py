from typing import cast

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from organizations.models import Organization
from organizations.serializers import OrganizationSerializer
from organizations.tests.factories import OrganizationFactory


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestReadOrganizationView:
    def test_retrieve_organization(self, api_client: APIClient) -> None:
        organization = OrganizationFactory()
        url = reverse("organizations:organization-detail", kwargs={"inn": organization.inn})
        response = cast(Response, api_client.get(url))

        assert response.status_code == status.HTTP_200_OK
        serializer = OrganizationSerializer(organization)
        assert response.data == serializer.data
        assert response.data["inn"] == organization.inn  # type: ignore
        assert response.data["balance"] == organization.balance  # type: ignore

    def test_retrieve_non_existent_organization(self, api_client: APIClient) -> None:
        url = reverse("organizations:organization-detail", kwargs={"inn": "123456789012"})
        response = cast(Response, api_client.get(url))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not_found" in str(response.data)

    def test_retrieve_invalid_inn_format(self, api_client: APIClient) -> None:
        url = reverse("organizations:organization-detail", kwargs={"inn": "invalid_inn"})
        response = cast(Response, api_client.get(url))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not_found" in str(response.data)
