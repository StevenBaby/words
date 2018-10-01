# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import os
import dandan
import logging
import datetime

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

    def set_time(self, time):
        current = timezone.localtime(time)
        logger.info("set system time to %s", current.strftime("%Y-%m-%d %H:%M:%S"))
        if dandan.system.is_win32():
            command = '''date {} && time {}'''.format(
                current.strftime("%m-%d-%y"),
                current.strftime("%H:%M:%S"))
        elif dandan.system.is_linux():
            command = '''echo {} | sudo -S date -s "{}"'''.format(
                self.PW,
                current.strftime("%Y-%m-%d %H:%M:%S"))
        os.system(command)

    def fit(self, count):
        if count > models.Review.objects.count():
            count = models.Review.objects.count()

        item = models.Review.objects.values("review_time").order_by("review_time")[count - 1]
        self.set_time(item["review_time"])

    def set(self):
        import requests
        import pytz
        try:
            res = requests.get("http://www.baidu.com", timeout=2)
            gmt = res.headers["Date"]
        except Exception:
            logger.warning("Cannot connect network, please check network connection and try again.")
            return
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        current = datetime.datetime.strptime(gmt, GMT_FORMAT).replace(tzinfo=pytz.timezone("GMT"))
        self.set_time(current)

    def handle(self, *args, **options):
        action = options["action"]
        count = options["count"]
        if "fit" == action:
            self.fit(count)
        if "set" == action:
            self.set()
