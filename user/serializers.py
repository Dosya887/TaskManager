from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
from django.core import signing
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User, OTP


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'role',
            'created_at',
            'is_active',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})

        validate_password(attrs['password1'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data.get('full_name', None),
            password=validated_data['password1'],
            is_active=False
        )
        return user

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password1', 'password2']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password
            )
            if not user:
                raise serializers.ValidationError('Пользователь не найден')
            if not user.is_active:
                raise serializers.ValidationError('Подтвердите почту для входа')
            attrs['user'] = user
            return attrs

        else:
            raise serializers.ValidationError('Почта и пароль обязательны')


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Пользователь не найден'})

        if user.is_active:
            raise serializers.ValidationError({'email': 'Почта уже подтверждена'})

        try:
            otp = OTP.objects.get(
                user=user,
                otp_code=otp_code,
                is_active=True,
                is_used=False
            )
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'otp_code': 'Неверный или не активный код'})

        if timezone.now() > otp.otp_created_at + timedelta(minutes=5):
            otp.is_active = False
            otp.save()
            raise serializers.ValidationError({'otp_code': 'Код ОТП истек'})

        attrs['user'] = user
        attrs['otp'] = otp
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError('Не валидный токен')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True,
                                         validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError('Неверно указан пароль')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('Новый пароль не совпадает')
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmOTPForChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Неверный код или email')

        try:
            otp = OTP.objects.get(
                user=user,
                otp_code=attrs['otp_code'],
                is_active=True,
                is_used=False
            )
        except OTP.DoesNotExist:
            raise serializers.ValidationError('Не правильный или не активный код')

        if timezone.now() > otp.otp_created_at + timedelta(minutes=5):
            raise serializers.ValidationError('Срок действия ОТП кода истек')

        otp.is_used = True
        otp.is_active = False
        otp.save()

        attrs['user'] = user
        return attrs


class ResetPasswordByEmailSerializer(serializers.Serializer):
    reset_token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают')

        try:
            data = signing.loads(
                attrs['reset_token'],
                salt='password-reset',
                max_age=timedelta(minutes=5)
            )
        except signing.SignatureExpired:
            raise serializers.ValidationError('reset_token истек')
        except signing.BadSignature:
            raise serializers.ValidationError('reset_token неверный')

        attrs['user_id'] = data['user_id']
        return attrs
