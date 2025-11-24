from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "avatar",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
            "groups",
        ]
        read_only_fields = ["id", "date_joined", "is_active"]

    def update(self, instance, validated_data):
        groups_data = validated_data.get("groups", [])

        if len(groups_data) > 1:
            # Prioritize Admin > Editor > Viewer and only set one group
            role = None
            for gp in groups_data:
                if gp.name == "Admin":
                    role = gp
                    break
                elif gp.name == "Editor":
                    role = gp
            if role:
                validated_data["groups"] = [role]

        if instance.is_active:
            instance.groups.set(validated_data.get("groups", []))
            instance.save()
            return instance
        return super().update(instance, validated_data)
