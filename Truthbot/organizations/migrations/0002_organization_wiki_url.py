# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-08 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='wiki_url',
            field=models.CharField(default=1, max_length=2083),
            preserve_default=False,
        ),
    ]
