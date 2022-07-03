import hashlib
import hmac
import base64
import time
import json
import requests
import random
from django.http import JsonResponse
from pytz import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import config.settings.my_settings as ENV
from django.conf import settings


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.created_at.astimezone(korean_timezone)

    @property
    def updated_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.updated_at.astimezone(korean_timezone)

    class Meta:
        abstract = True


class PhoneAuth(TimeStampModel):
    phone_number = models.CharField(max_length=11, primary_key=True)
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
            'content': "[짭포크 스토어] 인증 번호 [{}] 를 입력해주세요".format(self.auth_number),
            'messages': [{'to': self.phone_number}]
        }
        res = requests.post(
            ENV.SMS_URL, data=json.dumps(data), headers=headers)
        print(res.text)

    @classmethod
    def check_auth_number(cls, p_num, a_num):
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=a_num,
        )
        if result:
            return JsonResponse({
                "status": True,
                "message": "인증에 성공하셨습니다.",
                "result": "",
            }, status=200)
        return JsonResponse({
            "status": False,
            "message": "인증에 실패하셨습니다.",
            "result": "",
        }, status=401)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username,  name, birth_date, phone_number, tos_agree, password=None, **extra_fields):
        user = self.model(
            username=username,
            name=name,
            birth_date=birth_date,
            phone_number=phone_number,
            tos_agree=tos_agree,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, birth_date, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, name, birth_date, **extra_fields)


class User(AbstractUser, TimeStampModel):
    date_joined = None
    first_name = None
    last_name = None
    last_login = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=4)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=11, unique=True)
    tos_agree = models.BooleanField(default=True)
    sms_agree = models.BooleanField(default=False)
    email_agree = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'birth_date', 'phone_number']

    objects = UserManager()

    class Meta:
        db_table = 'users'
