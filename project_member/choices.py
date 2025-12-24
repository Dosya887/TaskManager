from django.db import models


class ProjectRole(models.TextChoices):
    """Роли пользователя в проекте."""

    OWNER = "owner", "Owner"
    MANAGER = "manager", "Manager"
    MEMBER = "member", "Member"
