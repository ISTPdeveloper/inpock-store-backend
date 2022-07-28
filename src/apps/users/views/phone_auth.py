from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from apps.core.regex import phone_number_validate
from apps.users.models.phone_auth import PhoneAuth


class AuthSmsSendAPI(APIView):

    def post(self, request):
        try:
            p_num = request.data['phone_number']
            phone_number_validate(p_num)
        except KeyError:
            return JsonResponse({
                "status": 'FAILURE',
                "message": "인증번호 발송에 실패하였습니다",
                "result": "",
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({
                "status": 'FAILURE',
                "message": "10자리 혹은 11자리 국내 휴대폰 번호를 입력해주세요",
                "result": ""
            })
        else:
            PhoneAuth.objects.update_or_create(phone_number=p_num)
            return JsonResponse({
                "status": 'SUCCESS',
                "message": "성공적으로 인증번호를 발송하였습니다",
                "result": "",
            }, status=200)


class AuthSmsVerifyAPI(APIView):

    def post(self, request):
        try:
            p_num = request.data['phone_number']
            a_num = request.data['auth_number']
        except KeyError:
            return JsonResponse({
                "status": 'FAILURE',
                "message": "인증번호가 일치하지 않습니다",
                "result": "",
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = PhoneAuth.check_auth_number(p_num, a_num)
            return result
