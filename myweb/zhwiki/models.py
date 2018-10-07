# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class WikiPaper(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    url = models.TextField(verbose_name="url", )

    class Meta:
        verbose_name = "词条"
        verbose_name_plural = "词条"

    def __str__(self):
        return self.__unicode__().encode("utf-8")

    def __unicode__(self):
        return self.title
