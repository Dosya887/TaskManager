from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task.permissions import IsTaskOwner, IsTaskExecutor
from task.serializers import TaskOwnerSerializer, TaskExecutorSerializer
from user.choices import Role


class TaskViewSet(ModelViewSet):
    """
    Задачи (Task).
    Требуется авторизация:
    Authorization: Bearer <access_token>
    Роли:
    - PROJECTMANAGER — создание и управление своими задачами
    - EXECUTOR — доступ только к назначенным задачам
    Методы:
    GET     /api/tasks/
    POST    /api/tasks/
    GET     /api/tasks/{id}/
    PUT     /api/tasks/{id}/
    PATCH   /api/tasks/{id}/
    DELETE  /api/tasks/{id}/
    """
    permission_classes = [IsAuthenticated, IsTaskExecutor | IsTaskOwner]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskOwnerSerializer

        user = self.request.user
        if user.role == Role.PROJECTMANAGER:
            return TaskOwnerSerializer
        return TaskExecutorSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
