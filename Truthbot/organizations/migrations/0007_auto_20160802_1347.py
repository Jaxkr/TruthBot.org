# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_auto_20160802_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='wiki',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.OrganizationWiki'),
        ),
    ]