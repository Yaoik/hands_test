import logging

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Organization
from .serializers import OrganizationSerializer

logger = logging.getLogger(__name__)


class ReadOrganizationView(GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = 'inn'
    lookup_url_kwarg = 'inn'

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
