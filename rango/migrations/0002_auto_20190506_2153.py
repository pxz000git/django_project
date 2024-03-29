# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2019-05-06 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='category',
            name='views',
            field=models.IntegerField(default=0, verbose_name='浏览数'),
        ),
    ]
