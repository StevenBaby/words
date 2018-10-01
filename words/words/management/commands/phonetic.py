# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand

import logging
from words import functions
from words import models


logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Get all phonetic in database'

    def handle(self, *args, **options):
        queryset = models.Word.objects.all().order_by("-id")
        for word in queryset:
            print(self.style.SUCCESS("download {}".format(word.title)))
            functions.download_word(word)
