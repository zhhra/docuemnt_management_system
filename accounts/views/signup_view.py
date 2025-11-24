from rest_framework import generics, permissions

from accounts.serializers import SignupSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [~permissions.IsAuthenticated]
