# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Paper(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


class ReadCount(models.Model):
    paper = models.ForeignKey(Paper, verbose_name="文章")
    read_count = models.IntegerField(verbose_name="阅读数")
    date = models.DateField(verbose_name="日期")
    good_count = models.IntegerField(verbose_name="点赞数", null=True, blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.paper.title, self.date)

    class Meta:
        verbose_name = '阅读量'
        verbose_name_plural = '阅读量'
        permissions = (("can_read_all", "Can Read All"),)  # work after makemigrations


class ReadCountSummary(ReadCount):
    class Meta:
        proxy = True
        verbose_name = "阅读量分析"
        verbose_name_plural = "阅读量分析"
        default_permissions = ('change',)  # add button not disappear
