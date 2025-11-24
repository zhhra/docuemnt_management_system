from rest_framework import serializers

from accounts.models import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2", "first_name", "last_name", "avatar"]

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError("Too long.")
        if CustomUser.objects.filter(email=value.lower(), is_active=True).exists():
            raise serializers.ValidationError("Not acceptable email.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user, _ = CustomUser.objects.update_or_create(
            **validated_data,
            defaults={"is_active": True},
        )
        user.set_password(password)
        user.save()
        return user
