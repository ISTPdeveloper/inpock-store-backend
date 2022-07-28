from django.urls import path
from .views import *


urlpatterns = [
    path('register', RegisterAPI.as_view(), name='user_register'),
    path('login', LoginAPI.as_view(), name='user_login'),
    path('logout', CustomBlacklistRefreshView.as_view(), name="logout"),

    path('sms', AuthSmsSendAPI.as_view(), name='sms_send'),
    path('sms/verify', AuthSmsVerifyAPI.as_view(), name='sms_verify'),

    path('register/seller', SellerRegisterAPI.as_view(), name='seller_register'),

    path('detail', CustomTokenVerifyView.as_view(), name='get_user'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
