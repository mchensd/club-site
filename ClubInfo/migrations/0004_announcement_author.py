# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 06:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ClubInfo', '0003_auto_20170909_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
