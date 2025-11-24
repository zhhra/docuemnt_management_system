from io import BytesIO

from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser


class UserAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("define_groups")
        cls.admin_group = Group.objects.get(name="Admin")
        cls.editor_group = Group.objects.get(name="Editor")
        cls.viewer_group = Group.objects.get(name="Viewer")
        cls.user = CustomUser.objects.create_user(
            email="test@test.com", password="Password123"
        )

    def setUp(self):
        self.users_url = reverse("users-list")
        self.signup_url = reverse("signup")

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)

    def get_avatar_file(self):
        file = BytesIO()
        image = Image.new("RGB", (100, 100), (155, 0, 0))
        image.save(file, "JPEG")
        file.seek(0)
        return SimpleUploadedFile("avatar.jpg", file.read(), content_type="image/jpeg")

    def test_signup_user(self):
        avatar_file = self.get_avatar_file()
        data = {
            "email": "newuser@test.com",
            "password": "NewPass123",
            "password2": "NewPass123",
            "first_name": "New",
            "last_name": "User",
            "avatar": avatar_file,
        }
        response = self.client.post(self.signup_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = CustomUser.objects.get(email="newuser@test.com")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.avatar.name.endswith(".jpg"))

    def test_create_user_as_admin(self):
        self.user.groups.add(self.admin_group)
        self.authenticate_user(self.user)

        avatar_file = self.get_avatar_file()
        data = {
            "email": "admin_created@test.com",
            "first_name": "Admin",
            "last_name": "User",
            "avatar": avatar_file,
            "groups": [self.viewer_group.id],
        }
        response = self.client.post(self.users_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_as_editor(self):
        self.user.groups.add(self.editor_group)
        self.authenticate_user(self.user)

        avatar_file = self.get_avatar_file()
        data = {
            "email": "editor_created@test.com",
            "first_name": "Editor",
            "last_name": "User",
            "password": "pass123",
            "avatar": avatar_file,
        }
        response = self.client.post(self.users_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users(self):
        self.user.groups.add(self.admin_group)
        self.authenticate_user(self.user)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("test@test.com", [u["email"] for u in response.data["results"]])

    def test_list_users_unauthenticated(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail(self):
        self.user.groups.add(self.admin_group)
        self.authenticate_user(self.user)
        response = self.client.get(reverse("users-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_user_detail_unauthenticated(self):
        response = self.client.get(reverse("users-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_user_as_admin(self):
        self.user.groups.add(self.admin_group)
        self.authenticate_user(self.user)

        # Active user
        active_user = CustomUser.objects.create_user(
            email="activeuser@test.com",
            password="pass",
            first_name="Old",
            last_name="Name",
            is_active=True,
        )

        avatar_file = self.get_avatar_file()
        data = {
            "first_name": "New",
            "last_name": "Name",
            "avatar": avatar_file,
            "groups": [self.editor_group.id],
        }

        response = self.client.patch(
            reverse("users-detail", args=[active_user.id]), data, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        active_user.refresh_from_db()
        self.assertEqual(list(active_user.groups.all()), [self.editor_group])
        self.assertEqual(active_user.first_name, "Old")
        self.assertEqual(active_user.last_name, "Name")
        self.assertFalse(active_user.avatar)

        # Inactive user
        inactive_user = CustomUser.objects.create_user(
            email="inactiveuser@test.com",
            password="pass",
            first_name="Old",
            last_name="Name",
            is_active=False,
        )
        avatar_file2 = self.get_avatar_file()
        data2 = {
            "first_name": "NewInactive",
            "last_name": "UserInactive",
            "avatar": avatar_file2,
            "groups": [self.admin_group.id], 
        }

        response2 = self.client.patch(
            reverse("users-detail", args=[inactive_user.id]), data2, format="multipart"
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        inactive_user.refresh_from_db()
        # All fields should be updated
        self.assertEqual(inactive_user.first_name, "NewInactive")
        self.assertEqual(inactive_user.last_name, "UserInactive")
        self.assertTrue(inactive_user.avatar.name.endswith(".jpg"))
        self.assertEqual(list(inactive_user.groups.values_list("id",flat=True)), [self.admin_group.id])

    def test_edit_user_for_viewer(self):
        self.user.groups.add(self.viewer_group)
        self.authenticate_user(self.user)

        target_user = CustomUser.objects.create_user(
            email="cannotedit@test.com", password="pass"
        )
        data = {"first_name": "Nope"}
        response = self.client.patch(
            reverse("users-detail", args=[target_user.id]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_admin(self):
        self.user.groups.add(self.admin_group)
        self.authenticate_user(self.user)

        target_user = CustomUser.objects.create_user(
            email="todelete@test.com", password="pass"
        )
        response = self.client.delete(reverse("users-detail", args=[target_user.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
