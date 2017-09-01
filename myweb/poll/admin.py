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
    empty_value_display = '-empty-'
    fields = ("paper", "read_count", 'good_count', "date")

    def view_good_count(self, obj):
        return obj.good_count

    view_good_count.empty_value_display = '???'


@admin.register(ReadCountSummary)
class ReadCountSummaryAdmin(ModelAdmin):
    list_display = ["date", "total_read_count"]
    ordering = ('-date',)
    list_per_page = 20

    def queryset(self, request):
        qs = super(ReadCountSummaryAdmin, self).queryset(request)
        new_qs = qs.values('date').annotate(total_date=Count('date'), read_count=Sum('read_count'),)
        return new_qs

    def total_read_count(self, obj):
        return obj.read_count

    total_read_count.short_description = '总阅读量'
    total_read_count.admin_order_field = 'read_count'

    # def hot_paper(self, obj):
    #     return obj.hot_paper
    #
    # hot_paper.short_description = "热门文章"
    # hot_paper.admin_order_field = "hot_paper"
