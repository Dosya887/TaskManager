from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Админ-панель для управления пользователями.
    Настроена для кастомной модели User с email вместо username.
    """
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'full_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('full_name', 'role')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('created_at', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    readonly_fields = ('created_at', 'last_login')
    filter_horizontal = ()


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления OTP кодами.
    Позволяет просматривать и управлять кодами подтверждения.
    """
    list_display = ('user_email', 'otp_code', 'is_active', 'is_used', 'otp_created_at', 'time_left')
    list_filter = ('is_active', 'is_used', 'otp_created_at')
    search_fields = ('user__email', 'otp_code')
    ordering = ('-otp_created_at',)
    readonly_fields = ('otp_created_at',)

    def user_email(self, obj):
        """Отображение email пользователя"""
        return obj.user.email

    user_email.short_description = 'Email пользователя'

    def time_left(self, obj):
        """Показывает оставшееся время действия кода"""
        from django.utils import timezone
        from datetime import timedelta

        if not obj.is_active:
            return "Неактивен"

        expiry_time = obj.otp_created_at + timedelta(minutes=5)
        time_remaining = expiry_time - timezone.now()

        if time_remaining.total_seconds() <= 0:
            return "Истек"

        minutes = int(time_remaining.total_seconds() // 60)
        seconds = int(time_remaining.total_seconds() % 60)
        return f"{minutes}м {seconds}с"

    time_left.short_description = 'Осталось времени'
