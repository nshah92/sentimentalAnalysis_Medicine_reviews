# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='favourite',
            field=models.BooleanField(default=False),
        ),
    ]
