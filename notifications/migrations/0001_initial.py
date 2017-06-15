# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 16:58
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
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=140)),
                ('notification_type', models.CharField(max_length=20)),
                ('relevant_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NotifiedUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.Notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='users',
            field=models.ManyToManyField(through='notifications.NotifiedUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]
