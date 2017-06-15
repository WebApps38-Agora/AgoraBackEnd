# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 18:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0002_comment_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='subscribers',
            field=models.ManyToManyField(related_name='comment_subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
