import hashlib
import hmac
import base64
import time
import json
from django.http import JsonResponse
import requests
import random
from django.db import models
from apps.core.models import TimeStampBaseModel
import config.settings.my_settings as ENV


class PhoneAuth(TimeStampBaseModel):
    phone_number = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    auth_number = models.IntegerField()

    class Meta:
        db_table = 'phone_auths'

    def make_signature(self, message):
        SECRET_KEY = bytes(ENV.SMS_SECRET_KEY, 'UTF-8')

        return base64.b64encode(hmac.new(SECRET_KEY, message, digestmod=hashlib.sha256).digest())

    def save(self, *args, **kwargs):
        self.auth_number = random.randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_message()

    def send_message(self):
        timestamp = str(int(time.time() * 1000))

        message = "POST " + ENV.SMS_URI + "\n" + timestamp + "\n" + ENV.SMS_ACCESS_KEY
        message = bytes(message, 'UTF-8')

        SIGNATURE = self.make_signature(message)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': ENV.SMS_ACCESS_KEY,
            'x-ncp-apigw-signature-v2': SIGNATURE,
        }

        data = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': ENV.SMS_CALLER,
            'content': "[인포크 스토어] 인증번호 [{}] 를 입력해주세요".format(self.auth_number),
            'messages': [{'to': self.phone_number}]
        }
        res = requests.post(
            ENV.SMS_URL, data=json.dumps(data), headers=headers)

    @classmethod
    def check_auth_number(cls, p_num, a_num):
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=a_num,
        )
        if result:
            return JsonResponse({
                "status": 'SUCCESS',
                "message": "인증에 성공하셨습니다",
                "result": {"phone_number": p_num},
            }, status=200)
        return JsonResponse({
            "status": 'FAILURE',
            "message": "인증에 실패하셨습니다",
            "result": "",
        }, status=401)
