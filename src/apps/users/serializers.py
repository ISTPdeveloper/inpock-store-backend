from rest_framework import serializers
from .models import PhoneAuth, User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name',
                  'birth_date', 'phone_number', 'tos_agree')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            phone_id = PhoneAuth.objects.get(
                phone_number=validated_data['phone_number'])
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                name=validated_data['name'],
                birth_date=validated_data['birth_date'],
                phone_number=validated_data['phone_number'],
                tos_agree=validated_data['tos_agree'],
                phone_auth=phone_id
            )
            return user
        except:
            raise serializers.ValidationError({
                "status": 'FAILURE',
                "message": "인증된 폰 번호가 아닙니다. 인증하신 폰 번호를 입력해주세요.",
                "result": ""
            })


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user

        raise serializers.ValidationError({
            "status": 'FAILURE',
            "message": "아이디 혹은 비밀번호가 잘못되었습니다. 다시 확인해주세요.",
            "result": ""
        })


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'birth_date', 'phone_number']


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs['refresh_token'])

            data = {
                "status": 'SUCCESS',
                "message": "",
                "result": {
                    'access_token': str(refresh.access_token),
                }
            }
            return data
        except:
            raise serializers.ValidationError({
                "status": 'FAILURE',
                "message": "토큰이 잘못되었거나 만료되었습니다.",
                "result": ""
            })
