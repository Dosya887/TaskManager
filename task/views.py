from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task.permissions import IsTaskOwner, IsTaskExecutor
from task.serializers import TaskOwnerSerializer, TaskExecutorSerializer
from user.choices import Role


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskExecutor | IsTaskOwner]

    def get_serializer_class(self):
        user = self.request.user

        if user.role == Role.PROJECTMANAGER:
            return TaskOwnerSerializer
        return TaskExecutorSerializer
