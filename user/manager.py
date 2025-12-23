from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User с email в качестве идентификатора.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с email и паролем.
        """
        if not email:
            raise ValueError('Почта обязателен для создание пользователя')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с email и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True")

        return self.create_user(email, password, **extra_fields)
