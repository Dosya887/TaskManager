from django.db import models


class TaskStatus(models.TextChoices):
    NEW = "новая","Новая"
    IN_PROGRESS = "в процессе", "В процессе"
    COMPLETED = "завершен", "Завершен"
