# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-01 10:26
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20161210_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=DjangoUeditor.models.UEditorField(verbose_name='机构描述'),
        ),
    ]
