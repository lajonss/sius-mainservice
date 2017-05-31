# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 23:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_app_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedapp',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usedapp',
            name='rating',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1),
        ),
        migrations.AlterField(
            model_name='usedapp',
            name='time_summary',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]