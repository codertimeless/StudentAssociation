# Generated by Django 2.2.8 on 2020-05-20 00:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20200519_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 20, 0, 16, 31, 801451)),
        ),
    ]