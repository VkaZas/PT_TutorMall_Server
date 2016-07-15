# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 07:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_courseinfo_orderinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinfo',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 7, 25, 10, 225694, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 7, 25, 16, 657287, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 11, 7, 25, 21, 236541, tzinfo=utc)),
            preserve_default=False,
        ),
    ]