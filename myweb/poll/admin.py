# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Paper, ReadCount


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
