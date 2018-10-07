# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime
import random

from django.http import HttpResponse


def create_count(request):
    from ..models import Paper, ReadCount

    Paper.objects.all().delete()
    ReadCount.objects.all().delete()

    def create_random_paper(count):

        for i in range(count):
            paper = Paper()
            paper.title = "第%d章" % i
            paper.content = "这是第 %d 章的内容" % i
            paper.save()

    def create_read_count(paper, end_date, days):
        this_date = end_date
        for _ in range(days):
            read = ReadCount()
            read.paper = paper
            read.read_count = random.randint(1, 100)
            read.date = this_date
            read.save()

            this_date -= datetime.timedelta(days=1)

    create_random_paper(10)
    end_date = datetime.date.today()

    for paper in Paper.objects.all():
        create_read_count(paper, end_date, 20)

    return HttpResponse("OK")
