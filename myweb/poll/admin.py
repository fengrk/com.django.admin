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
    change_list_template = 'admin/read_count_summary_change_list.html'
    list_per_page = 2

    _queryset = ReadCountSummary.objects.values('date') \
        .annotate(total_date=Count('date'), read_count=Sum('read_count')) \
        .order_by("date")

    def changelist_view(self, request, extra_context=None):
        response = super(ReadCountSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            queryset = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # response.context_data['cl'].queryset = queryset = ReadCount.objects.values('date') \
        #     .annotate(total_date=Count('date'), read_count=Sum('read_count')) \
        #     .order_by("date")

        summary = []

        for result in queryset:
            result["paper"] = ReadCount.objects.filter(date=result["date"]).order_by("-read_count").first()
            summary.append(result.copy())

        response.context_data["summary"] = summary

        return response

    def get_queryset(self, request):
        return self._queryset

    def get_changelist(self, request, **kwargs):
        _queryset = self._queryset

        class MyChangeList(ChangeList):
            def get_queryset(self, request):
                return _queryset
        return MyChangeList
