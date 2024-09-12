# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import os
import dandan
import logging
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from words import models


logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Set OS time from internet'

    PW = "kang"

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            "-a",
            type=str,
            required=True,
            help="action type",
            choices=['set', 'fit', ])
        parser.add_argument('--count', '-c', type=int, default=20, help="count of review")

    def fit(self, count):
        if count > models.Review.objects.count():
            count = models.Review.objects.count()

        item = models.Review.objects.values("review_time").order_by("review_time")[count - 1]
        delta = item["review_time"] - timezone.now()
        user = User.objects.get(id=1)
        user.profile.settings_timedelta = delta
        user.save()
        logger.info("Time forward to %s", 
                    (timezone.localtime() + delta).strftime("%Y-%m-%d %H:%M:%S"))

    def set(self):
        now = timezone.now()
        delta = now - now
        user = User.objects.get(id=1)
        logger.info("Time forward %s seconds", delta.seconds)
        user.profile.settings_timedelta = delta
        user.save()

    def handle(self, *args, **options):
        action = options["action"]
        count = options["count"]
        if "fit" == action:
            self.fit(count)
        if "set" == action:
            self.set()
