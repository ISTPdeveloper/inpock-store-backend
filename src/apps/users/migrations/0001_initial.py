# Generated by Django 4.0.5 on 2022-07-28 16:09

import apps.users.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('tos_agree', models.BooleanField(default=True)),
                ('sms_agree', models.BooleanField(default=False)),
                ('email_agree', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', apps.users.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('auth_number', models.IntegerField()),
            ],
            options={
                'db_table': 'phone_auths',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_registration_number', models.CharField(max_length=100, verbose_name='?????????????????????')),
                ('company_name', models.CharField(max_length=100, verbose_name='?????????')),
                ('company_owner_name', models.CharField(max_length=100, verbose_name='????????????')),
                ('company_location', models.CharField(max_length=100, verbose_name='??????????????????')),
                ('bank_name', models.CharField(choices=[('????????????', '1'), ('????????????', '2'), ('??????', '3'), ('????????????', '4'), ('??????', '5'), ('????????????', '6'), ('????????????', '7'), ('????????????', '8'), ('?????????', '9'), ('????????????', '10'), ('????????????', '11'), ('????????????', '12'), ('????????????', '13'), ('????????????', '14'), ('????????????', '15'), ('???????????????', '16'), ('??????', '17'), ('????????????', '18'), ('????????????', '19'), ('????????????', '20'), ('??????', '21'), ('????????????', '22')], max_length=5, verbose_name='?????????')),
                ('account_holder_name', models.CharField(max_length=100, verbose_name='????????????')),
                ('account_number', models.CharField(max_length=100, verbose_name='????????????')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'seller',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='phone_auth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.phoneauth'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
