# Generated by Django 4.0.5 on 2022-07-06 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_phone_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_auth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.phoneauth'),
        ),
    ]