# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_remove_post_file_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]
