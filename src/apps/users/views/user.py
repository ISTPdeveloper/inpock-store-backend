from django.http import JsonResponse
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers.user import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "status": True,
            "message": "회원가입에 성공했어요",
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
            "message": "로그인에 성공했어요",
            "result": {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        }, status=200)
