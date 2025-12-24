from django.contrib import admin

from project_member.models import ProjectMember


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    """Админка для участников проекта (ProjectMember)"""

    list_display = (
        'id',
        'user',
        'project',
        'role',
    )

    list_display_links = ('id', 'user')

    list_filter = ('role', 'project')

    search_fields = (
        'user__username',
        'user__email',
        'project__title',
    )

    autocomplete_fields = ('user', 'project')

    ordering = ('project', 'role')

    readonly_fields = ()

    fieldsets = (
        (None, {
            'fields': ('user', 'project', 'role')
        }),
    )
