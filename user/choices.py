from django.db import models


class Role(models.TextChoices):
    """
    Роли пользователей в системе управления задачами.

    Роли:
        - PROJECTMANAGER: Менеджер проекта (создает задачи, управляет командой)
        - ADMIN: Администратор (полный доступ ко всем функциям системы)
        - EXECUTOR: Исполнитель (выполняет назначенные задачи)

    Использование:
        user.role = Role.EXECUTOR
        if user.role == Role.ADMIN:
            # предоставить админские права
    """
    PROJECTMANAGER = "project manager", "Project Manager"
    ADMIN = "admin", "Admin"
    EXECUTOR = "executor", "Executor"
