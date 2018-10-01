# coding=utf-8
from __future__ import print_function, unicode_literals
from django.core.management.base import BaseCommand

# from words import functions
# from words import statistics
# import six
import logging
import webbrowser
# import datetime

from django.utils import timezone
# from django.db.models import Q

from words import models
from words import functions


logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Run test functions'

    def handle(self, *args, **options):
        edited = {}

        queryset = models.Paraphrase.objects.extra(
            where=['content REGEXP %s and content REGEXP %s '],
            params=[r'^[\S]*$', r'.*][^ ].*'],
        ).filter(
            word__review__isnull=False,
        ).distinct().order_by("-word__review__review_time")
        count = queryset.count()
        print("Count %s" % count)
        while True:
            count -= 1
            if count < 0:
                break
            para = queryset[count]
            word = para.word

            if word.title in edited:
                continue
            edited[word.title] = True
            url = "http://steven-arch.local/zh-hans/edit/{}/".format(para.word.id)
            review = para.word.review.first()
            if review:
                review_time = timezone.localtime(review.review_time)
            else:
                review_time = timezone.now()

            print(self.style.SUCCESS("{} {} {}".format(review_time.strftime("%Y-%m-%d %H"), para.word.title, url)))
            try:
                key = ord(functions.getch())
                if key == 101:
                    return
                webbrowser.open_new_tab(url)
            except Exception:
                print(Exception)
