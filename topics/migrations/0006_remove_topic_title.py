# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 23:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0005_auto_20170601_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='title',
        ),
    ]
