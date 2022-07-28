from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.core.models import TimeStampBaseModel
from apps.users.models.phone_auth import PhoneAuth


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username,  name, birth_date, phone_number, tos_agree, password=None):
        user = self.model(
            username=username,
            name=name,
            birth_date=birth_date,
            phone_number=phone_number,
            tos_agree=tos_agree,
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


class User(AbstractUser, TimeStampBaseModel):
    date_joined = None
    first_name = None
    last_name = None
    last_login = models.DateTimeField(null=True, blank=True)

    email = models.EmailField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=100, unique=True)
    tos_agree = models.BooleanField(default=True)
    sms_agree = models.BooleanField(default=False)
    email_agree = models.BooleanField(default=False)
    phone_auth = models.ForeignKey(
        PhoneAuth, null=False, blank=False, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = UserManager()

    class Meta:
        db_table = 'users'
