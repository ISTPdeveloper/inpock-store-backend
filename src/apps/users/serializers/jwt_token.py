from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


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
            raise serializers.ValidationError("토큰이 잘못되었거나 만료되었어요")
