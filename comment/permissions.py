from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCommentWriteOrRead(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        task = obj.task

        if request.method in SAFE_METHODS:
            return (
                task.created_by == user or task.executor == user
            )

        return obj.author == user
