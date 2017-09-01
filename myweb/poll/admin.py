# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Count

from models import Paper, ReadCount, ReadCountSummary


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    fields = ('title', 'content')


@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    fields = ("paper", "read_count", 'good_count', "date")
    list_display = ("paper", "read_count", 'view_good_count', "date")
    list_per_page = 20

    def view_good_count(self, obj):
        return obj.good_count

    view_good_count.empty_value_display = '-'
    view_good_count.short_description = '赞数'
    view_good_count.admin_order_field = 'good_count'


@admin.register(ReadCountSummary)
class ReadCountSummaryAdmin(ModelAdmin):
    list_display = ["date", "all_count", 'hot_paper']
    search_fields = ('date', )
    ordering = ('-date',)
    list_per_page = 20

    def queryset(self, request):
        return super(ReadCountSummaryAdmin, self).queryset(request)

    def all_count(self, obj):
        if obj.good_count:
            return "%d/%d" % (obj.read_count, obj.good_count)
        else:
            return "%d/0" % obj.read_count

    all_count.short_description = '阅读量/赞数'
    all_count.admin_order_field = None  # None: 不排序;　'read_count': 以 read_count 参数排序

    def hot_paper(self, obj):
        try:
            return self.model.objects.filter(date=obj.date).order_by("-read_count").first().paper
        except:
            return '-'

    hot_paper.short_description = "热门文章"
