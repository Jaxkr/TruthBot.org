# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 06:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_auto_20160804_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='news.Comment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentvote',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]