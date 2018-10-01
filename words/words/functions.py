# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import os
import six
import re
import glob
import shutil
import dandan
import random
import logging
import logging.config

from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# from django.db.models import F
# from django.db.models import Count

from words import models
from utils import youdao
from words import styles


logger = logging.getLogger('words')


def show_console_log(show=True):
    logging.shutdown()
    config = dandan.value.AttrDict(settings.LOGGING)
    if show:
        config.handlers.console["class"] = 'logging.StreamHandler'
    else:
        config.handlers.console["class"] = 'logging.NullHandler'
    logging.config.dictConfig(config)


def exists(title):

    return models.Word.objects.filter(title__iexact=title).exists()


def equals(word, title):

    return word.equals.filter(title__iexact=title).exists()


def similars(word, title):

    return word.similars.filter(title=title).exists()


def get_random(queryset):
    count = queryset.count()
    if count == 0:
        return None
    index = random.randint(0, count - 1)
    return queryset[index]


def split(line):
    line = line.strip()
    line, num = re.subn(' +', ' ', line)
    titles = line.split("|")
    return titles


def input(prompt=""):
    try:
        line = six.moves.input(prompt).strip()
    except KeyboardInterrupt:
        exit(-1)
    return split(line)


def getch():
    try:
        return dandan.system.getch()
    except KeyboardInterrupt:
        exit(-1)


def print_paras(word):
    if isinstance(word, dandan.value.AttrDict):
        for para in word.paras:
            print(styles.TITLE("{}.{}".format(para.type, para.content), True))
    elif isinstance(word, models.Word):
        for para in word.paraphrase.all():
            print(styles.TITLE(str(para), True))


def prints(word):
    print(settings.SPLITTER)
    print(styles.TITLE(word.title, True))
    print(settings.SPLITTER)
    print_paras(word)
    print(settings.SPLITTER)


@transaction.atomic
def save(result, word=None):
    if settings.IGNORED_PATTERN.match(result.title):
        return
    if not word:
        type = models.WordType.objects.get_or_create(content=result.type)[0]
        word, created = models.Word.objects.get_or_create(
            title=result.title,
            type=type)
        if result.create_time:
            word.create_time = result.create_time
        if created:
            word.save()

    word.star = result.star

    # phonetic
    for phon in result.phonetics:
        type = models.PhoneticType.objects.get_or_create(content=youdao.PHONETICS[phon.type])[0]
        phonetic = word.phonetic.filter(type=type).first()
        if phonetic:
            phonetic.content = phon.content
            phonetic.save()
        else:
            models.Phonetic.objects.get_or_create(content=phon.content, type=type, word=word)[0]

    # rank
    for content in result.ranks:
        rank = models.Rank.objects.get_or_create(content=content)[0]
        rank.word.add(word)

    for para in result.paras:
        type = models.ParaType.objects.get_or_create(content=para.type)[0]
        models.Paraphrase.objects.get_or_create(content=para.content, type=type, word=word)

    word.save()

    # if not isinstance(result.level, int):
    #     return word
    # if result.level < 0:
    #     return word
    # user = User.objects.get(id=1)
    # review = models.Review.objects.get_or_create(word=word, user=user)[0]
    # review.level = result.level
    # review.hard = result.hard
    # review.times = result.times
    # review.error = result.error
    # result.skip = result.skip
    # review.first_time = result.first_time.replace(tzinfo=timezone.get_current_timezone())
    # review.update_time = result.update_time.replace(tzinfo=timezone.get_current_timezone())
    # review.review_time = result.review_time.replace(tzinfo=timezone.get_current_timezone())
    # review.save()

    return word


def refresh(word):
    result = youdao.get_word(word.title)
    if not result:
        return None
    word.refresh_time = timezone.now()
    word = save(result, word)
    return word


def get_user(user=1):
    if isinstance(user, int):
        return User.objects.get(id=user)
    return user


@transaction.atomic
def set_review(word, user=1):

    return models.Review.objects.get_or_create(word=word, user=get_user(user))


def get_all_review(user=1):
    if isinstance(user, int):
        user = User.objects.get(id=user)
    return models.Review.objects.filter(user=user)


@transaction.atomic
def reset_review(review):
    review.reset += 1
    review.level = 0
    review.update_time = timezone.now()
    review.review_time = timezone.now()
    review.save()


def get_word(title):
    word = models.Word.objects.filter(title=title).first()
    if word:
        return word

    return models.Word.objects.filter(title__iexact=title).first()


def get_review(word, user):
    if not isinstance(word, models.Word):
        return
    return get_all_review(user).filter(word=word).first()


def get_phonetic_content(word, type):
    if isinstance(word, models.Word):
        phonetic = word.phonetic.filter(type__content__iexact=type).first()
        if phonetic and phonetic.content:
            return phonetic.content
    elif isinstance(word, dandan.value.AttrDict):
        for phonetic in word.phonetics:
            if phonetic.description == type and phonetic.content:
                return phonetic.content
    return ""


def consult(title):
    word = models.Word.objects.filter(title=title).first()
    if word:
        return word

    word = youdao.get_word(title)
    if not word:
        return word

    if models.Word.objects.filter(title=word.title).exists():
        word = models.Word.objects.filter(title=word.title).first()
        return word

    word.create_time = timezone.now()
    word.refresh_time = timezone.now()
    return word


def get_backups():
    filename = os.path.join(settings.BACKUP_PATH, "*words.db")
    return sorted(glob.glob(filename), reverse=True)


def backup():
    filename = "{}_{}".format(timezone.localtime(timezone.now()).strftime("%Y_%m_%d_%H_%M_%S"), "words.db")
    backupname = os.path.join(settings.BACKUP_PATH, filename)
    logger.info("Copy database from %s to %s", settings.DATABASE_PATH, backupname)
    shutil.copy2(settings.DATABASE_PATH, backupname)

    filename = os.path.join(settings.BACKUP_PATH, "*words.db")
    files = sorted(glob.glob(filename), reverse=True)[settings.BACKUP_COUNT:]
    for filename in files:
        try:
            logger.info("Remove older backup %s", filename)
            os.remove(filename)
        except Exception:
            continue
    return backupname


def restore(filename=None):
    files = get_backups()
    if not files:
        logger.warning("There are no any backup")
        return
    if filename not in files:
        filename = files[0]
    logger.info("Copy database backup from %s to %s", filename, settings.DATABASE_PATH)
    shutil.copy2(filename, settings.DATABASE_PATH)


def download_phonetic(phonetic):
    title = phonetic.word.title
    if os.path.exists(phonetic.filename):
        return phonetic.filename, False

    if phonetic.type.content == "UK":
        type = youdao.PHONETIC_UK
    elif phonetic.type.content == "US":
        type = youdao.PHONETIC_US

    youdao.get_phonetic(title=title, filename=phonetic.filename, type=type)
    if os.path.exists(phonetic.filename):
        return phonetic.filename, True
    return "", False


def download_word(word):
    if word.type.content == "EN":
        for var in youdao.PHONETICS:
            content = youdao.PHONETICS[var]
            type = models.PhoneticType.objects.get_or_create(content=content)[0]
            phon = models.Phonetic.objects.get_or_create(type=type, word=word)[0]
            download_phonetic(phon)
    else:
        raise ValueError("word type error")


def play_phonetic(phonetic):
    filename, _ = download_phonetic(phonetic)
    player = os.path.join(settings.BASE_DIR, "utils", "player.py")
    command = '''{} "{}"'''.format(player, filename)
    os.system(command)


def play_word(word, index):
    index = index % word.phonetic.count()
    phonetic = word.phonetic.all()[index]
    play_phonetic(phonetic)
    return phonetic
