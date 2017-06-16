# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0002_auto_20170614_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='subscribers',
            field=models.ManyToManyField(related_name='topic_subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]