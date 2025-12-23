from django.contrib import admin
from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для модели Task"""

    # Поля, отображаемые в списке
    list_display = (
        'id',
        'title',
        'project',
        'status',
        'executor',
        'created_by',
        'deadline',
        'created_at',
        'updated_at',
    )

    # Ссылки на редактирование через клик
    list_display_links = ('id', 'title')

    # Поля, по которым можно фильтровать список
    list_filter = ('status', 'project', 'executor', 'created_by')

    # Поля для поиска
    search_fields = ('title', 'description', 'executor__username', 'created_by__username')

    # Read-only поля
    readonly_fields = ('created_at', 'updated_at')

    # Сортировка по умолчанию
    ordering = ('-created_at',)

    # Сгруппировать поля на форме редактирования
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'project', 'status', 'executor')
        }),
        ('Дополнительно', {
            'fields': ('created_by', 'deadline', 'created_at', 'updated_at')
        }),
    )

    # Авто-установка создателя при сохранении в админке
    def save_model(self, request, obj, form, change):
        if not change:  # Только при создании
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
