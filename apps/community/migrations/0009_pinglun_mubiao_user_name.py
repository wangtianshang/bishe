# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-06 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_auto_20190405_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='pinglun',
            name='mubiao_user_name',
            field=models.CharField(default=1, max_length=20, verbose_name='用户名字'),
            preserve_default=False,
        ),
    ]