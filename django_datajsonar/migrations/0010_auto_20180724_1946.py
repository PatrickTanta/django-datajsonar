# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-24 19:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_datajsonar', '0009_auto_20180718_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='last_reviewed',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='admins',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
