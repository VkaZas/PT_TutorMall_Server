# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 08:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Info',
            new_name='UserInfo',
        ),
    ]