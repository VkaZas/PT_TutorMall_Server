# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('server', '0004_delete_connectuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectUser',
            fields=[
                ('uuid', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('QQnumber', models.CharField(max_length=20)),
                ('PayUser', models.CharField(max_length=20)),
                ('PayPSW', models.CharField(max_length=20)),
            ],
        ),
    ]
