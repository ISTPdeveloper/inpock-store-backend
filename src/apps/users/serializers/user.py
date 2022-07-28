from rest_framework import serializers
from apps.core.regex import name_validate, password_validate, phone_number_validate, username_validate
from django.contrib.auth import authenticate
from apps.users.models.phone_auth import PhoneAuth

from apps.users.models.user import User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'name',
                  'birth_date', 'phone_number', 'tos_agree')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, validated_data):
        username_validate(validated_data['username'])
        password_validate(validated_data['password'])
        name_validate(validated_data['name'])
        phone_number_validate(validated_data['phone_number'])

        return validated_data

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
                phone_auth=phone_id,
            )

            return user
        except PhoneAuth.DoesNotExist:
            raise serializers.ValidationError(
                "인증된 폰 번호가 아닙니다. 인증하신 폰 번호를 입력해주세요")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user

        raise serializers.ValidationError("아이디 혹은 비밀번호가 일치하지 않아요")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'birth_date', 'phone_number']
