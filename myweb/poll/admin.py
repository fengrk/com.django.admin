# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum

from poll.forms import AuthorForm
from .models import Paper, ReadCount, ReadCountSummary, Author, Author2, Book

logger = logging.getLogger("django")


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    fields = ("title", "content", "update_time")
    list_display = ("title", "content", "update_time")
    readonly_fields = ['update_time']


@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    fields = ("paper", "read_count", 'good_count', "date")
    list_display = ("paper", "read_count", 'view_good_count', "has_good_count", "human_date")
    list_per_page = 20
    ordering = ('-date',)
    list_editable = ("read_count",)
    change_list_template = "admin/readcount_change_list.html"

    def view_good_count(self, obj):
        if obj.good_count is None:
            return "<a style='color: red;'>-</a>"
        return obj.good_count

    view_good_count.empty_value_display = '-'
    view_good_count.allow_tags = True  # html safe
    view_good_count.short_description = '赞数'
    view_good_count.admin_order_field = 'good_count'

    def has_good_count(self, obj):
        return obj.good_count is not None

    has_good_count.boolean = True
    has_good_count.short_description = '有赞'

    def human_date(self, obj):
        return str(obj.date)

    human_date.short_description = '日期'
    human_date.admin_order_field = 'date'


@admin.register(ReadCountSummary)
class ReadCountSummaryAdmin(ModelAdmin):
    change_list_template = 'admin/read_count_summary_change_list.html'
    list_per_page = 10
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

    def countchart_view(self, request, extra_context=None):
        _template = "admin/read_count_summary_chart_count.html"

        # context = {}
        #
        # cl = {"opts": {"app_label": "poll", "app_config": {"verbose_name": "测试栏目"}, "verbose_name_plural": "报表分析"}}
        # context["cl"] = cl
        #
        # return render_to_response(_template, RequestContext(request, context))
        response = super(ReadCountSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        x_data = []
        y_data = []

        for record in ReadCount.objects.values("date").annotate(read_count=Sum('read_count'), ).order_by("date"):
            x_data.append(str(record["date"]))
            y_data.append(record["read_count"])

        response.context_data["x_data"] = x_data
        response.context_data["y_data"] = y_data
        response.template_name = _template
        return response

    def form_test_vew(self, request, extra_context=None):
        from django import forms

        _template = "poll/django-example.html"

        response = super(ReadCountSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        class PaperForm(forms.ModelForm):
            class Meta:
                model = Paper
                fields = ('title', 'content',)

        response.context_data["action_url"] = "/poll/paper/add/"
        response.context_data["form"] = PaperForm()
        response.template_name = _template
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

            def get_results(self, request):
                if not hasattr(self, "_got_result"):
                    setattr(self, "_got_result", super(MyChangList, self).get_results(request))
                return getattr(self, "_got_result")

        return MyChangList

    def get_urls(self):
        urlpatterns = super(ReadCountSummaryAdmin, self).get_urls()

        # 所有url跳转至 changelist
        new_urlpatterns = []
        changelist_urlpattern = urlpatterns[0]
        new_urlpatterns.append(changelist_urlpattern)

        info = self.model._meta.app_label, self.model._meta.model_name

        new_urlpatterns.append(url(r'^chart/count/$',
                                   self.admin_site.admin_view(self.countchart_view), name='%s_%s_countchart' % info), )

        new_urlpatterns.append(url(r'^form/test/$',
                                   self.admin_site.admin_view(self.form_test_vew), name='%s_%s_form_test' % info), )

        for urlpattern in urlpatterns[1:]:
            urlpattern.callback = changelist_urlpattern.callback
            new_urlpatterns.append(urlpattern)

        return new_urlpatterns


class AuthorAdmin(ModelAdmin):
    form = AuthorForm
    fields = ("nick_name", "user_name", "password", "password1")
    list_display = ("user", "nick_name")


class BookInline(admin.TabularInline):
    model = Book


class Author2Admin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Author2, Author2Admin)
