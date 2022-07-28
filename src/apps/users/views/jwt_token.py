from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers.jwt_token import CustomTokenRefreshSerializer
from apps.core.decorators import auth_decorator


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class CustomTokenVerifyView(APIView):
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


class CustomBlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh_token'))
        token.blacklist()
        return JsonResponse({
            "status": 'SUCCESS',
            "message": "로그아웃에 성공하셨습니다",
            "result": "",
        }, status=200)
