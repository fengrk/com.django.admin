# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Paper(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __unicode__(self):
        return self.title


class ReadCount(models.Model):
    paper = models.ForeignKey(Paper, verbose_name="文章")
    read_count = models.IntegerField(verbose_name="阅读数")
    date = models.DateField(verbose_name="日期")
    good_count = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.paper.title, self.date)
