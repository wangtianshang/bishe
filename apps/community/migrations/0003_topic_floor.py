# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-03 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20190402_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='floor',
            field=models.IntegerField(default=0, verbose_name='层级'),
        ),
    ]
