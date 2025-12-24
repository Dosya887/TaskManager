from django.contrib import admin
from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев к задачам."""

    list_display = ('id', 'task', 'author', 'text', 'created_at')

    list_display_links = ('id', 'task', 'author')

    list_filter = ('task', 'author')

    search_fields = ('text', 'author__username', 'task__title')

    readonly_fields = ('created_at', 'author')

    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('task', 'author', 'text')
        }),
        ('Дополнительно', {
            'fields': ('created_at',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
