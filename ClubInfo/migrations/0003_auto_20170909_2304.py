# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 06:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ClubInfo', '0002_auto_20170828_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fake_col', models.CharField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
        migrations.AlterField(
            model_name='score',
            name='taker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClubInfo.Profile'),
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
