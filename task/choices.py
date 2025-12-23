from django.db import models


class TaskStatus(models.TextChoices):
    """Статусы задачи: Новая, В процессе, Завершена"""
    NEW = "новая","Новая"
    IN_PROGRESS = "в процессе", "В процессе"
    COMPLETED = "завершен", "Завершен"
