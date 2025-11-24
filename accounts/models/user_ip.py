from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserIP(models.Model):
    ip = models.GenericIPAddressField()
