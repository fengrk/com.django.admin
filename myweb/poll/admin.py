# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum

from models import Paper, ReadCount, ReadCountSummary

logger = logging.getLogger("django")


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    fields = ('title', 'content')


@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    fields = ("paper", "read_count", 'good_count', "date")
    list_display = ("paper", "read_count", 'view_good_count', "date")
    list_per_page = 5
    ordering = ('-date',)

    def view_good_count(self, obj):
        return obj.good_count

    view_good_count.empty_value_display = '-'
    view_good_count.short_description = '赞数'
    view_good_count.admin_order_field = 'good_count'

    def get_queryset(self, request):
        qs = super(ReadCountAdmin, self).get_queryset(request)
        return qs.filter(date__gt=datetime.date(2017, 8, 30))


@admin.register(ReadCountSummary)
class ReadCountSummaryAdmin(ModelAdmin):
    change_list_template = 'admin/read_count_summary_change_list.html'
    list_per_page = 2
    ordering = ("-date",)

    def changelist_view(self, request, extra_context=None):
        response = super(ReadCountSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        change_list = response.context_data['cl']
        change_list.get_results(request)
        object_list = change_list.result_list

        summary = []

        for result in object_list:
            logger.info(result)
            result["paper"] = ReadCount.objects.filter(date=result["date"]).order_by("-read_count").first()
            summary.append(result.copy())

        response.context_data["summary"] = summary

        return response

    def get_queryset(self, request):
        ReadCount.objects.all()
        qs = super(ReadCountSummaryAdmin, self).get_queryset(request)
        new_qs = qs.values("date").annotate(read_count=Sum('read_count'), )
        return new_qs

    def get_changelist(self, request, **kwargs):
        class MyChangList(ChangeList):
            def get_ordering(self, request, queryset):
                # todo ChangeList中, 加入 pk 排序，导致 group by 出错
                # ordering = super(MyChangList, self).get_ordering(request, queryset)
                #
                # ordering_set = set(ordering)
                # for _pk in ("pk", "-pk"):
                #     if _pk in ordering_set:
                #         ordering_set.remove(_pk)
                return ['-date']

        return MyChangList
