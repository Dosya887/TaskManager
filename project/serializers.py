from project.models import Project
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'owner', 'created_at']
