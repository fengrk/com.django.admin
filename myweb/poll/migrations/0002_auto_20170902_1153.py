# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-02 03:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadCountSummary',
            fields=[
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': '\u9605\u8bfb\u91cf\u5206\u6790',
                'proxy': True,
                'verbose_name_plural': '\u9605\u8bfb\u91cf\u5206\u6790',
            },
            bases=('poll.readcount',),
        ),
        migrations.AlterModelOptions(
            name='paper',
            options={'verbose_name': '\u6587\u7ae0', 'verbose_name_plural': '\u6587\u7ae0'},
        ),
        migrations.AlterModelOptions(
            name='readcount',
            options={'permissions': (('can_read_all', 'Can Read All'),), 'verbose_name': '\u9605\u8bfb\u91cf', 'verbose_name_plural': '\u9605\u8bfb\u91cf'},
        ),
    ]
