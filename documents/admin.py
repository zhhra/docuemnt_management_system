from django.contrib import admin

from documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "uploaded_by", "uploaded_at", "is_public")
    list_filter = ("is_public", "uploaded_at")
    search_fields = (
        "title",
        "description",
        "uploaded_by__first_name",
        "uploaded_by__last_name",
    )
    readonly_fields = ("uploaded_at", "updated_at")
    raw_id_fields = ("initiator", "uploaded_by")
