# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 11:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='wiki',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.OrganizationWiki'),
        ),
    ]