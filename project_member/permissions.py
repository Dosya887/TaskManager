from rest_framework.permissions import BasePermission

from project_member.choices import ProjectRole
from project_member.models import ProjectMember


class IsProjectOwnerOrManager(BasePermission):

    def has_object_permission(self, request, view, obj):
        return ProjectMember.objects.filter(
            user=request.user,
            project=obj.project,
            role__in=(ProjectRole.MANAGER, ProjectRole.OWNER)
        ).exists()
