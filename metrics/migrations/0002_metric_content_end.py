# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='content_end',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]