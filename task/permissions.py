from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from user.choices import Role


class IsTaskOwner(BasePermission):
    message = 'Это не ваш проект'

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.PROJECTMANAGER and obj.created_by == request.user


class IsTaskExecutor(BasePermission):
    message = 'Вы не имеете доступ к этой задаче'

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.EXECUTOR and obj.executor == request.user
