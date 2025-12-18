from rest_framework import serializers

from task.models import Task


class TaskOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')


class TaskExecutorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'status',)
