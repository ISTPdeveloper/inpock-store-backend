from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from apps.users.serializers import *
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PhoneAuth
from . import auth_decorator
from rest_framework_simplejwt.views import TokenRefreshView
# Create your views here.


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "status": True,
            "message": "회원가입에 성공하셨습니다.",
            "result": {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        }, status=200)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "status": 'SUCCESS',
            "message": "로그인에 성공하셨습니다.",
            "result": {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        }, status=200)


class AuthSmsSendAPI(APIView):

    def post(self, request):
        try:
            p_num = request.data['phone_number']
        except KeyError:
            return JsonResponse({
                "status": 'FAILURE',
                "message": "인증번호 발송에 실패하였습니다.",
                "result": "",
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            PhoneAuth.objects.update_or_create(phone_number=p_num)
            return JsonResponse({
                "status": 'SUCCESS',
                "message": "성공적으로 인증번호를 발송하였습니다.",
                "result": "",
            }, status=200)


class AuthSmsVerifyAPI(APIView):

    def get(self, request):
        try:
            p_num = request.query_params['phone_number']
            a_num = request.query_params['auth_number']
        except KeyError:
            return JsonResponse({
                "status": 'FAILURE',
                "message": "인증번호 인증에 실패하였습니다.",
                "result": "",
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = PhoneAuth.check_auth_number(p_num, a_num)
            return result


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class CustomTokenVerifyView(generics.RetrieveAPIView):

    @auth_decorator.auth
    def get(self, request):
        user = request.user
        return JsonResponse({
            "status": 'SUCCESS',
            "message": "",
            "result": {
                'id': user.id,
                'name': user.name,
                'username': user.username,
            }
        }, status=200)
