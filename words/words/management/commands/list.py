# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand
import dandan

import logging
from django.utils import timezone
from words import statistics
from words import functions
from words import study


logger = logging.getLogger("words")

class Command(BaseCommand):
    help = 'Show review word first date count each day in the past'

    def add_arguments(self, parser):
        parser.add_argument('type', nargs="?", type=str, default='review', help="list type")

    def handle(self, *args, **options):
        type = options['type']
        if type == 'hard':
            queryset = study.get_hard()
        elif type == 'review':
            queryset = study.get_review()
        else:
            logging.warning("type %s unknown", type)
            return

        for var in queryset:
            print(var.word.title, end=' ')
        print()
