# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-10 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_datajsonar', '0003_auto_20180508_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='distribution',
            name='new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='field',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
