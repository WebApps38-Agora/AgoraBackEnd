# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='source',
            name='url',
            field=models.URLField(max_length=300),
        ),
        migrations.AlterField(
            model_name='source',
            name='url_logo',
            field=models.URLField(max_length=300),
        ),
    ]