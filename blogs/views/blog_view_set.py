from rest_framework import viewsets

from base_app.permissions import StrictModelPermission
from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [StrictModelPermission]
