# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 16:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
