# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0003_auto_20170530_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]