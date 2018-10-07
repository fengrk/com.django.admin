# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import WikiPaper


class WikiPaperAdmin(admin.ModelAdmin):
    fields = ("title", "content",)
    list_display = ("title", "content",)
    search_fields = ("title",)

    def __init__(self, *args, **kwargs):
        super(WikiPaperAdmin, self).__init__(*args, **kwargs)
        from zhwiki.sources.migrate_tools import migrate_wiki_data
        migrate_wiki_data()


admin.site.register(WikiPaper, WikiPaperAdmin)
