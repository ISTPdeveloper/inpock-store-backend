from django.db import models
from apps.core.enums import BANK_NAME_CHOICES
from apps.core.models.timestamp import TimeStampBaseModel
from apps.users.models.user import User


class Seller(TimeStampBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_registration_number = models.CharField(
        max_length=100, verbose_name='사업자등록번호')
    company_name = models.CharField(max_length=100, verbose_name='상호명')
    company_owner_name = models.CharField(
        max_length=100, verbose_name='대표자명')
    company_location = models.CharField(
        max_length=100, verbose_name='사업자소재지')
    bank_name = models.CharField(
        max_length=5, choices=BANK_NAME_CHOICES, verbose_name='은행명')
    account_holder_name = models.CharField(
        max_length=100, verbose_name='예금주명')
    account_number = models.CharField(
        max_length=100, verbose_name='계좌번호')

    REQUIRED_FIELDS = ['companyOwnerName', 'company_name', 'company_owner_name',
                       'company_location', 'bank_name', 'account_holder_name', 'account_number']

    class Meta:
        db_table = 'seller'
