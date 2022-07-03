import jwt
from django.http import JsonResponse
from .models import User
import config.settings.my_settings as ENV


def auth(func):
    def wrapper(self, request, **kwargs):
        auth_token = request.headers.get("Authorization", None)
        auth_token = str.replace(str(auth_token), 'Bearer ', '')
        if auth_token == None:
            return JsonResponse({
                "status": False,
                "message": "토큰을 입력해주세요.",
                "result": "",
            }, status=401)

        try:
            payload = jwt.decode(
                auth_token, ENV.JWT_SECRET_KEY, algorithms=['HS256'])

            if User.objects.get(id=payload['user_id']):
                user = User.objects.get(id=payload['user_id'])
                request.user = user
                return func(self, request, **kwargs)

        except:
            return JsonResponse({
                "status": False,
                "message": "토큰이 잘못되었거나 만료되었습니다.",
                "result": "",
            }, status=401)

    return wrapper
