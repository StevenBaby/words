# encoding=utf-8
from __future__ import print_function, unicode_literals, division
# import os
# import six
# import re
# import glob
# import shutil
# import dandan
import logging

# from django.db import transaction
# from django.conf import settings
from django.utils import timezone
# from django.contrib.auth.models import User
# from django.db.models import F
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.functions import TruncHour

from words import functions
from words import models

logger = logging.getLogger('words')


def get_word_count():
    return models.Word.objects.all().count()


def get_review_count(user):
    return functions.get_all_review(user=functions.get_user(user)).count()


def get_level_count(user=1):

    return functions.get_all_review(user=functions.get_user(user))\
        .values("level")\
        .annotate(count=Count('level'))\
        .order_by("-level")


def get_level(level, user=1):

    return functions.get_all_review(user=functions.get_user(user))\
        .filter(level=level)\
        .order_by("review_time")


def get_error_count(user=1):

    return functions.get_all_review(user=functions.get_user(user))\
        .values("error")\
        .annotate(count=Count('error'))\
        .order_by("-error")


def get_error(error, user=1):

    return functions.get_all_review(user=functions.get_user(user))\
        .filter(error=error)\
        .order_by("review_time")


def get_coming(user=1):
    return functions.get_all_review(user=functions.get_user(user))\
        .annotate(date=TruncDate('review_time'))\
        .values("date")\
        .annotate(count=Count('id'))\
        .order_by("date")


def get_count(user=1):
    return functions.get_all_review(user=functions.get_user(user))\
        .annotate(date=TruncDate('first_time'))\
        .values("date")\
        .annotate(count=Count('id'))\
        .order_by("-date")


def get_date(date=None, user=1):
    if not date:
        date = timezone.localtime(timezone.now()).date()

    return functions.get_all_review(user=functions.get_user(user))\
        .annotate(date=TruncDate('review_time'))\
        .filter(date=date)\
        .annotate(hour=TruncHour('review_time'))\
        .values("hour")\
        .annotate(count=Count('id'))\
        .order_by("hour")


def get_date_count(date=None, user=1):
    if not date:
        date = timezone.localtime(timezone.now()).date()

    return functions.get_all_review(user=functions.get_user(user))\
        .annotate(date=TruncDate('review_time'))\
        .filter(date=date).count()
