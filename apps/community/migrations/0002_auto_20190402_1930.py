# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-02 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='topic_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.Node', verbose_name='所属节点'),
        ),
    ]
