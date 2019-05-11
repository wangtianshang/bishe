# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-04 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_coursepanduantest_coursetiankongtest'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSorce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.IntegerField(verbose_name='所属课程')),
                ('user', models.IntegerField(verbose_name='所属用户')),
                ('sorce', models.CharField(max_length=100, verbose_name='分数')),
            ],
            options={
                'verbose_name': '测试题分数',
                'verbose_name_plural': '测试题分数',
            },
        ),
    ]