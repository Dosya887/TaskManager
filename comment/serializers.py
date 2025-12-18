from rest_framework import serializers

from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'task', 'text', 'created_at', 'author']
        read_only_fields = ['author', 'task']
