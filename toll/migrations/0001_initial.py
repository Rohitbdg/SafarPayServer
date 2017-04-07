# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_id', models.CharField(editable=False, max_length=30, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('Name', models.CharField(max_length=40)),
                ('Mobile', models.CharField(max_length=10)),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=20)),
                ('rto_balance', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]