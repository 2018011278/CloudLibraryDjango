# Generated by Django 3.1.2 on 2020-11-06 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 12, 26, 2, 856877), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 12, 26, 2, 856877), verbose_name='创建时间'),
        ),
    ]