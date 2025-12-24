from django.contrib import admin
from project.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Админка для модели Project"""

    list_display = ('id', 'title', 'owner', 'created_at')

    list_display_links = ('id', 'title')

    list_filter = ('owner',)

    search_fields = ('title', 'description', 'owner__username', 'owner__email')

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'owner')
        }),
        ('Дополнительно', {
            'fields': ('created_at',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
