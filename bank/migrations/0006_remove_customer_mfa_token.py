# Generated by Django 3.2.7 on 2022-06-01 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_auto_20220601_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='mfa_token',
        ),
    ]