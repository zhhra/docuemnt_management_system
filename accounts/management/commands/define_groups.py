from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Setup initial groups and permissions"

    def handle(self, *args, **options):
        # Permissions for Document model
        view_doc = Permission.objects.get(codename="view_document")
        add_doc = Permission.objects.get(codename="add_document")
        change_doc = Permission.objects.get(codename="change_document")
        delete_doc = Permission.objects.get(codename="delete_document")

        # 1. Admin group (all permissions + some user/group permissions)
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        user_perms = Permission.objects.filter(
            codename__in=["view_customuser", "add_customuser", "change_customuser"]
        )
        admin_group.permissions.set(
            list(user_perms) + [view_doc, add_doc, change_doc, delete_doc]
        )

        # 2. Editor group
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_group.permissions.set([view_doc, add_doc, change_doc])

        # 3. Viewer group (view only)
        viewer_group, _ = Group.objects.get_or_create(name="Viewer")
        viewer_group.permissions.set([view_doc])

        self.stdout.write(self.style.SUCCESS("Groups and permissions created!"))
