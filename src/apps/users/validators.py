import re

from django.forms import ValidationError

REGEX = {
    'USERNAME': '^[a-z0-9$@$!%*#?&]{4,20}$',
    'PASSWORD': '^(?=.*[a-z])(?=.*\d)[a-z\d]{8,20}$',
    'NAME': '^[가-힣]{2,4}$',
    'PHONE_NUMBER': '01[0-1, 7][0-9]{7,8}$'
}


def username_validate(username):
    if not re.match(REGEX['USERNAME'], username):
        raise ValidationError({
            "status": 'FAILURE',
            "message": "아이디 양식에 맞게 입력해주세요",
            "result": ""
        })


def password_validate(password):
    if not re.match(REGEX['PASSWORD'], password):
        raise ValidationError({
            "status": 'FAILURE',
            "message": "패스워드 양식에 맞게 입력해주세요",
            "result": ""
        })


def name_validate(name):
    if not re.match(REGEX["NAME"], name):
        raise ValidationError({
            'status': 'FAILURE',
            "message": "올바른 이름을 입력해주세요.",
            "result": ""
        })


def phone_number_validate(phone_number):
    if not re.match(REGEX["PHONE_NUMBER"], phone_number):
        raise ValidationError({
            "status": 'FAILURE',
            "message": "10자리 혹은 11자리 국내 휴대폰 번호를 입력해주세요",
            "result": ""
        })
