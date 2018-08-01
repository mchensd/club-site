# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-31 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClubInfo', '0012_auto_20171030_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='score',
            name='taker',
        ),
        migrations.AddField(
            model_name='contest',
            name='out_of',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='contest',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
