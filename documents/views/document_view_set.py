from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from base_app.permissions import StrictModelPermission
from documents.models import Document
from documents.serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_public", "uploaded_by"]
    search_fields = ["title", "description"]
    ordering_fields = ["uploaded_at", "title"]
    ordering = ["-uploaded_at"]
    permission_classes = [StrictModelPermission]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user, initiator=self.request.user)
