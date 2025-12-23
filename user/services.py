from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from user.models import User, OTP
import random


@shared_task
def send_otp_code(user_id):
    """
        Отправляет пользователю одноразовый код подтверждения (OTP) на email.
        Параметры:
            user_id (int): ID пользователя, которому отправляется код.
        Логика:
            - Генерирует случайный 6-значный код
            - Сохраняет код и время его создания в объекте пользователя
            - Отправляет email с кодом пользователю
        Возвращает:
            str: OTP код, если пользователь найден
            str: сообщение об ошибке, если пользователь не найден
        """

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found"

    OTP.objects.filter(user=user, is_active=True).update(is_active=False)

    otp_code = str(random.randint(100000, 999999))

    OTP.objects.create(
        user=user,
        otp_code=otp_code,
        is_active=True,
        is_used=False
    )

    send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения: {otp_code}",
        settings.EMAIL_HOST_USER,
        [user.email]
    )

    return otp_code
