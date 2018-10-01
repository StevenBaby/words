# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand

import six
import logging
from django.utils import timezone

from words import functions
from words import models

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Refresh all word in database base on refresh_time'

    def handle(self, *args, **options):
        refresh_time = timezone.datetime(2017, 11, 27, 18).replace(tzinfo=timezone.get_current_timezone())
        logger.info("Refresh word %s", refresh_time)
        queryset = models.Word.objects.filter(type__content="EN", refresh_time__lt=refresh_time)
        words = [var for var in queryset]
        count = len(words)
        for index in six.moves.range(0, count):
            word = words[index]
            logger.info("Refresh word (%s/%s) %s", index + 1, count, word.title)
            try:
                functions.refresh(word)
            except KeyboardInterrupt:
                exit(0)
