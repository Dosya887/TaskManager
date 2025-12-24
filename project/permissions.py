from rest_framework.permissions import BasePermission, SAFE_METHODS

from project.models import Project
from project_member.choices import ProjectRole
from project_member.models import ProjectMember


class IsProjectManager(BasePermission):
    """Разрешение для менеджеров и владельцев проекта; SAFE_METHODS для всех участников."""
    message = 'Вы не являетесь менеджером проекта'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return ProjectMember.objects.filter(
                project=obj,
                user=request.user,
            ).exists()

        return ProjectMember.objects.filter(
            project=obj,
            user=request.user,
            role__in=(ProjectRole.MANAGER, ProjectRole.OWNER),
        ).exists()

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(member__user=user)
