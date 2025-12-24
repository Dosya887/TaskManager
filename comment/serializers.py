from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Комментарий к задаче с read-only автором и задачей."""

    class Meta:
        model = Comment
        fields = ['id', 'task', 'text', 'created_at', 'author']
        read_only_fields = ['author', 'task']
