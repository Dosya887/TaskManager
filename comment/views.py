from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from comment.models import Comment
from comment.permissions import IsCommentWriteOrRead
from comment.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentWriteOrRead]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            task__created_by=user
        ) | Comment.objects.filter(
            task__executor=user
        )

    def perform_create(self, serializer):
        user = self.request.user
        task = serializer.validated_data['task']

        if user != task.created_by and user != task.executor:
            raise PermissionDenied("You don't have access to this task")
        serializer.save(author=user)
