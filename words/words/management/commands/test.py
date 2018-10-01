# coding=utf-8
from django.core.management.base import BaseCommand

import logging

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Run test functions'

    def handle(self, *args, **options):
        # from words import models
        pass
