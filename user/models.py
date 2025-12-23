from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from user.choices import Role
from user.manager import CustomUserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name="Почта")
    full_name = models.CharField(max_length=255, verbose_name="Имя", null=True, blank=True)
    role = models.CharField(max_length=100, choices=Role.choices, default=Role.EXECUTOR,
                            verbose_name="Роль")
    is_active = models.BooleanField(default=False, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создание аккаунта")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} - {self.role}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otp_codes",
                                verbose_name="Пользователь")
    otp_code = models.CharField(max_length=6, verbose_name="ОТП код")
    otp_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создание ОТП")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_used = models.BooleanField(default=False, verbose_name="Использован")

    def __str__(self):
        return f"{self.user.email} - {self.otp_code} - {'Активен' if self.is_active else 'Неактивен'}"

    class Meta:
        verbose_name = "ОТП код"
        verbose_name_plural = "ОТП коды"
        ordering = ["-otp_created_at"]

