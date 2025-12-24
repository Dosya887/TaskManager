from rest_framework import serializers

from project_member.models import ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    """Сериализатор для управления участниками проекта и их ролями."""

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'project', 'role']
        read_only_fields = ['id', 'user']
