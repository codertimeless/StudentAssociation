# Generated by Django 2.2.8 on 2020-05-19 23:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20200519_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 23, 8, 52, 876949)),
        ),
    ]