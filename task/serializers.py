from rest_framework import serializers

from task.models import Task


class TaskOwnerSerializer(serializers.ModelSerializer):
    """
    Сериализатор задачи для владельца (PROJECTMANAGER).
    Полный доступ к данным задачи.
    """
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')


class TaskExecutorSerializer(serializers.ModelSerializer):
    """
    Сериализатор задачи для исполнителя (EXECUTOR).
    Доступ только к статусу задачи.
    """
    class Meta:
        model = Task
        fields = ('id', 'status',)
