from rest_framework import serializers

from documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.SerializerMethodField()
    initiator = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "description",
            "file",
            "initiator",
            "uploaded_by",
            "uploaded_at",
            "updated_at",
            "is_public",
        ]
        read_only_fields = ["initiator", "uploaded_by", "uploaded_at", "updated_at"]

    def get_uploaded_by(self, obj):
        uploaded_by = obj.uploaded_by
        return uploaded_by.user_info() if uploaded_by else None

    def get_initiator(self, obj):
        initiator = obj.initiator
        return initiator.user_info() if initiator else None

    def update(self, instance, validated_data):
        file = validated_data.get("file")
        if file:
            instance.uploaded_by = self.context["request"].user
            instance.file = file
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance
