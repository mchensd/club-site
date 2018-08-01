# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-31 04:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClubInfo', '0014_auto_20171030_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('out_of', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='contest',
            name='out_of',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='score',
        ),
        migrations.AddField(
            model_name='score',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClubInfo.Contest'),
        ),
        migrations.AddField(
            model_name='score',
            name='taker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClubInfo.Profile'),
        ),
    ]
