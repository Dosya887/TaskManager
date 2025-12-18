from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


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
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password1', 'password2']


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

        if user.otp_code != otp_code:
            raise serializers.ValidationError({'otp_code': 'Введен не правильный код'})

        if timezone.now() > user.otp_created_at + timedelta(minutes=5):
            raise serializers.ValidationError({'otp_code': 'Код ОТП истек'})

        attrs['user'] = user
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
            raise serializers.ValidationError({'token': 'Не валидный токен'})
