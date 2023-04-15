# coding=utf-8
from django.core.management.base import BaseCommand

import logging

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Print words version'

    def handle(self, *args, **options):
        # from words import models
        import words
        print(words.__version__)
