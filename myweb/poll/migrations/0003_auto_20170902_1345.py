# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-02 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_auto_20170902_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readcount',
            name='good_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u70b9\u8d5e\u6570'),
        ),
    ]