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
    change_list_template = 'admin/read_count_summary_change_list.html'
    ordering = ('-date',)
    list_per_page = 5

    def changelist_view(self, request, extra_context=None):
        extra_context = {}
        summary = []
        for record in self.get_queryset(request):
            summary.append({
                "date": record["date"],
                "read_count": record["read_count"],
                "paper": self.model.objects.filter(date=record["date"]).order_by("-read_count").first().paper}
            )

        extra_context["summary"] = summary
        return super(ReadCountSummaryAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        ReadCount.objects.all()
        qs = super(ReadCountSummaryAdmin, self).get_queryset(request)
        new_qs = qs.values("date").annotate(read_count=Sum('read_count'), )
        return new_qs
