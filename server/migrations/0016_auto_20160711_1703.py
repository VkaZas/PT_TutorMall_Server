# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 09:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0015_auto_20160711_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinfo',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 11, 9, 3, 54, 927408)),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 11, 9, 3, 54, 929450)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 11, 9, 3, 54, 924400)),
        ),
    ]
