# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand
import dandan
from words import statistics
from words import functions


class Command(BaseCommand):
    help = 'Show review word count each hour today'

    def handle(self, *args, **options):
        functions.show_console_log(False)
        items = statistics.get_date()

        for item in items:
            item = dandan.value.AttrDict(item)
            print("{hour:0>2} {count:>3}".format(
                hour=item.hour.hour,
                count=item.count
            ))
