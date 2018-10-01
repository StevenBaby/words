# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand
import dandan

from django.utils import timezone
# from django.db.models import Count
# from django.db.models.functions import TruncDate

# from words import models
from words import statistics
from words import functions


class Command(BaseCommand):
    help = 'Show review word count each day in the future'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs="?", type=int, default=10, help="count of days")

    def handle(self, *args, **options):
        functions.show_console_log(False)
        count = options["count"]

        items = statistics.get_coming()[:count]

        items = [item for item in items]
        items.reverse()

        today = timezone.localtime(timezone.now()).date()
        for item in items:
            item = dandan.value.AttrDict(item)
            print("{offset:0>2} {date} {count:>3} {weekday}".format(
                offset=(item.date - today).days,
                date=item.date,
                count=item.count,
                weekday=item.date.strftime("%A")
            ))
