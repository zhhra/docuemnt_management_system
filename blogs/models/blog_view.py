from django.db import models


class BlogView(models.Model):
    blog = models.ForeignKey(
        "blogs.Blog", on_delete=models.SET_NULL, null=True, related_name="views"
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="read_blogs",
    )
    user_ip = models.ForeignKey(
        "accounts.UserIP",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="read_blogs",
    )
