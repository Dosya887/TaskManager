from django.db import models


class Role(models.TextChoices):
    PROJECTMANAGER = "project manager", "Project Manager"
    ADMIN = "admin", "Admin"
    EXECUTOR = "executor", "Executor"
