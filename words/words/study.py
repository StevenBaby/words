# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import logging
import datetime

from django.utils import timezone
from django.db import transaction
# from django.conf import settings
# from django.contrib.auth.models import User
from django.db.models import F
# from django.db.models import Count

import dandan

from words import models
from words import functions

from words import interval


logger = logging.getLogger('words')


def check(word, titles, save=True):
    data = dandan.value.AttrDict()
    data.list = []
    data.title = word.title
    data.paras = word.paraphrases()

    equal = False
    right = False
    error = False
    for title in titles:
        title = title.strip()
        if len(title) < 2:
            continue

        item = dandan.value.AttrDict()
        item.title = title
        item.error = False
        item.right = False
        item.equal = False
        item.exists = False
        item.paras = []

        if title == word.title:
            equal = True
            item.equal = True
            item.paras = data.paras

        elif functions.equals(word, title):
            right = True
            item.right = True
            item.paras = functions.get_word(title).paraphrases()

        elif title.lower().replace(" ", "") == word.title.lower().replace(" ", ""):
            right = True
            item.right = True
            item.paras = data.paras

        elif functions.exists(title):
            exists = functions.get_word(title)
            item.exists = True
            item.paras = exists.paraphrases()
            # if not functions.similars(word, title):
            if save:
                word.similars.add(exists)
                word.save()
        else:
            error = True
            item.error = True

        data.list.append(item)

    if not right and not equal:
        error = True

    data.equal = equal
    data.right = right
    data.error = error
    return data


# review functions
def update_hard(review):
    delta = interval.interval(review.level)
    if review.hard > 0:
        period = delta / (review.hard + 1)
        review.hard_time = review.update_time + period
    else:
        review.hard = 0


def get_review(user=1):
    return functions.get_all_review(user=user)\
        .filter(review_time__lte=timezone.now())\
        .filter(update_time__lt=timezone.now() - datetime.timedelta(seconds=1))


def get_review_count(user=1):
    if hasattr(user, 'review_count'):
        return user.review_count

    count = get_review(user=user).count()
    if isinstance(user, int):
        return count

    user.review_count = count
    return count


def has_review(user=1):

    return get_review(user=user).first() is not None


def can_review(word, user=1):

    return get_review(user=user).filter(word=word).exists()


def set_skip(user=1):
    skiped = functions.get_all_review(user=user)\
        .filter(review__gt=0).update(review=0, skip=F("skip") + 1)
    logger.debug("skiped review count %s", skiped)


@transaction.atomic
def get_random_review(user=1):
    set_skip(user=user)
    review = functions.get_random(get_review(user=user))
    if not review:
        return review
    review.times += 1
    review.review = 1
    review.save()
    return review


def get_near_review(user=1):
    return functions.get_all_review(user=user)\
        .filter(update_time__lt=timezone.now() - datetime.timedelta(seconds=1))\
        .order_by("review_time").first()


@transaction.atomic
def review_right(word=None, user=1):
    review = get_review(user=user).filter(word=word).first()
    if not review:
        return

    logger.debug("review right %s", word)
    review.level += 1
    review.review = 0
    review.right += 1
    review.update_time = timezone.now()

    delta = interval.interval(review.level)
    review.review_time = review.update_time + delta
    update_hard(review)
    review.save()


@transaction.atomic
def review_error(word=None, user=1):
    review = get_review(user=user).filter(word=word).first()
    if not review:
        return

    logger.debug("review error %s", word)
    review.hard += 1
    review.error += 1
    review.review = 0
    if ' ' in word.title and review.level >= 1:
        review.level -= 1
    elif review.level >= 2:
        review.level -= 2
    review.update_time = timezone.now()

    update_hard(review)
    review.save()


# hard function

def get_hard(user=1):
    return functions.get_all_review(user=user)\
        .exclude(hard=0)\
        .exclude(review_time__lte=timezone.now())\
        .filter(review_time__gt=F('hard_time'))\
        .filter(hard_time__lte=timezone.now())


def get_hard_count(user=1):
    if hasattr(user, 'hard_count'):
        return user.hard_count

    count = get_hard(user=user).count()
    if isinstance(user, int):
        return count

    user.hard_count = count
    return count


def has_hard(user=1):

    return get_hard(user).first() is not None


def can_hard(word, user=1):

    return get_hard(user=user).filter(word=word).exists()


def get_near_hard(user=1):
    return functions.get_all_review(user=user)\
        .exclude(hard=0)\
        .exclude(review_time__lte=timezone.now())\
        .filter(review_time__gt=F('hard_time'))\
        .order_by("hard_time").first()


def get_random_hard(user=1):
    # return get_hard(user).order_by("?").first()
    return functions.get_random(get_hard(user))


@transaction.atomic
def hard_right(word=None, user=1):
    review = get_hard(user=user).filter(word=word).first()
    if not review:
        return

    logger.debug("hard error %s", word)
    review.hard -= 1
    update_hard(review)
    review.save()


@transaction.atomic
def hard_error(word=None, user=1):
    review = get_hard(user=user).filter(word=word).first()
    if not review:
        return

    logger.debug("hard error %s", word)
    review.hard += 1
    update_hard(review)
    review.save()


def get_practice(user=1):

    return models.Word.objects.exclude(
        id__in=functions.get_all_review(user).values("word")
    )


def get_practice_count(user=1):

    return get_practice(user).count()


def has_practice(user=1):

    return get_practice(user).first() is not None


def can_practice(word, user=1):

    return get_practice(user).filter(id=word.id).exists()


def get_random_practice(user=1):

    # return get_practice(user).order_by("?").first()
    return functions.get_random(get_practice(user))
