# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 02:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IOTapp', '0003_device_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='cur_temp',
            new_name='temperature',
        ),
        migrations.RemoveField(
            model_name='device',
            name='temp_string',
        ),
        migrations.RemoveField(
            model_name='device',
            name='time_string',
        ),
    ]
