# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alignment', models.CharField(max_length=30)),
                ('profession', models.CharField(max_length=30)),
                ('town', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('profile_picture', models.URLField(max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
