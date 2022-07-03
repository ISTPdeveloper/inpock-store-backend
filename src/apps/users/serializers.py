import json
from os import access
from django.conf import settings
from django.http import JsonResponse
from rest_framework import serializers

from apps.users import auth_decorator
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenVerifySerializer


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name',
                  'birth_date', 'phone_number', 'tos_agree')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            birth_date=validated_data['birth_date'],
            phone_number=validated_data['phone_number'],
            tos_agree=validated_data['tos_agree'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user

        raise serializers.ValidationError({
            "status": False,
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
                "status": True,
                "message": "",
                "result": {
                    'access_token': str(refresh.access_token),
                }
            }
            return data
        except:
            raise serializers.ValidationError({
                "status": False,
                "message": "토큰이 잘못되었거나 만료되었습니다.",
                "result": ""
            })


class CustomTokenVerifySerializer(serializers.Serializer):
    @auth_decorator.auth
    def validate(self, attrs):

        return {
            "message": "The token is verified and can be used.",
        }
