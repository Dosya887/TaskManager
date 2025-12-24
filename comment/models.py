from django.db import models

from task.models import Task
from user.models import User


class Comment(models.Model):
    """Комментарий к задаче с автором, текстом и датой создания."""
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE,
        verbose_name="Задача", related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Автор", related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.task} - {self.text}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ('-created_at',)
