# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_auto_20160709_2113'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ConnectUser',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
