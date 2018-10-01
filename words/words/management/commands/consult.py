# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand
# from django.conf import settings

import logging
# import dandan
from words import functions
# from words import models

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Consult word in database or internet'

    def add_arguments(self, parser):
        parser.add_argument('title', nargs="+", type=str)

    def handle(self, *args, **options):
        functions.show_console_log(False)
        title = " ".join(options["title"])
        word = functions.consult(title)
        if word:
            functions.prints(word)
        else:
            print(self.style.ERROR("Consult {} failure".format(title)))
