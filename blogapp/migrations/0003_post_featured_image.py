# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20171124_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured_image',
            field=models.CharField(default='', max_length=384),
        ),
    ]
