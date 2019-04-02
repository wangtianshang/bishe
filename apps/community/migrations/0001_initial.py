# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-02 18:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='节点名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '节点',
                'verbose_name_plural': '节点',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='话题名')),
                ('content', models.TextField(max_length=100, verbose_name='话题内容')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击数')),
                ('number', models.IntegerField(default=0, verbose_name='评论数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('topic_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.Node', verbose_name='课程机构')),
            ],
            options={
                'verbose_name': '话题',
                'verbose_name_plural': '话题',
            },
        ),
    ]