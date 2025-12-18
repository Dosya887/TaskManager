from django.db import models

from project.models import Project
from user.models import User
from task.choices import TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    description = models.TextField(verbose_name="Описание", blank=True)
    status = models.CharField(max_length=33, choices=TaskStatus.choices,default=TaskStatus.NEW,
                              verbose_name="Статус")
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Исполнитель", related_name="executor_tasks")
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name="Создатель", related_name="created_tasks")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ["-created_at"]
