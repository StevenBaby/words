# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand
import dandan

from django.utils import timezone
from words import statistics
from words import functions


class Command(BaseCommand):
    help = 'Show review word first date count each day in the past'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs="?", type=int, default=10, help="count of days")

    def handle(self, *args, **options):
        functions.show_console_log(False)
        count = options["count"]
        items = statistics.get_count()[:count]

        items = [item for item in items]
        items.reverse()

        today = timezone.now().date()
        for item in items:
            item = dandan.value.AttrDict(item)
            print("{offset:0>2} {date} {count:>3} {weekday}".format(
                offset=(today - item.date).days,
                date=item.date,
                count=item.count,
                weekday=item.date.strftime("%A")
            ))
