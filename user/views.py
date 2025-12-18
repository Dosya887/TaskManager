from django.contrib.auth import login, authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.services import send_otp_code
from user.serializers import (RegisterSerializer,
                              VerifyOTPSerializer,
                              LogoutSerializer, LoginSerializer
                              )


class RegisterApiView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_otp_code.delay(user.id)
        return Response({'message': 'ОТП код отправлен на почту',
                         'email': user.email}, status=status.HTTP_201_CREATED)


class VerifyOtpApiView(APIView):

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user.is_active = True
        user.otp_code = None
        user.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({'message': 'Почта успешна подтверждена',
                         'refresh': str(refresh),
                         'access': str(access),
                         'email': user.email,
                         'full_name': user.full_name
                         }, status=status.HTTP_200_OK)


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Вы успешно вошли в систему',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Вы вышли с аккаунта'}, status=status.HTTP_200_OK)
