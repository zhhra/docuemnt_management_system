from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from base_app.permissions import StrictModelPermission


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter()
    serializer_class = CustomUserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["date_joined", "first_name", "last_name"]
    ordering = ["-date_joined"]
    permission_classes = [StrictModelPermission]
