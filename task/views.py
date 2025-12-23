from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task.permissions import IsTaskOwner, IsTaskExecutor
from task.serializers import TaskOwnerSerializer, TaskExecutorSerializer
from user.choices import Role


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsTaskExecutor | IsTaskOwner]

    def get_queryset(self):
        user = self.request.user

        if user.role == Role.PROJECTMANAGER:
            return Task.objects.filter(created_by=user)
        return Task.objects.filter(executor=user)

    def get_serializer_class(self):
        user = self.request.user

        if user.role == Role.PROJECTMANAGER:
            return TaskOwnerSerializer
        return TaskExecutorSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(created_by=user)
