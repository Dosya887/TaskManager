from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from user.choices import Role
from user.manager import CustomUserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name="Почта")
    full_name = models.CharField(max_length=255, verbose_name="Имя", null=True, blank=True)
    role = models.CharField(max_length=100, choices=Role.choices, default=Role.EXECUTOR,
                            verbose_name="Роль")
    otp_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="ОТП код")
    otp_created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
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
        ordering = ['-created_at']
