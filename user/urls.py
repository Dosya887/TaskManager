from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from user.views import (
    RegisterApiView, LogoutApiView, LoginApiView, PasswordResetRequestView,
    ConfirmOTPForChangePasswordView, ResetPasswordByEmailView, ChangePasswordApiView
)

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('password-reset/', ChangePasswordApiView.as_view(), name='password_reset'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm-otp/', ConfirmOTPForChangePasswordView.as_view(), name='password-reset-confirm-otp'),
    path('password-reset/reset/', ResetPasswordByEmailView.as_view(), name='password-reset-reset'),
]
