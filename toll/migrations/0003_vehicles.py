# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 06:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('toll', '0002_toll'),
    ]

    operations = [
        migrations.CreateModel(
            name='vehicles',
            fields=[
                ('vehicle_no', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('vehicle_type', models.PositiveIntegerField()),
                ('special_vehicle', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toll.users')),
            ],
        ),
    ]