# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand
import sys
import logging
import dandan

from django.utils import timezone
from django.db import transaction
from django.conf import settings

from words import functions
from words import models
from words import status
from words import styles
from words import study

logger = logging.getLogger("words")


class DictationMethod(object):
    name = "base"
    short_name = "b"
    help = "Base metho for study"
    index = 0

    def right(self, item):
        pass

    def error(self, item):
        pass

    def skip(self, item):
        pass

    def para(self, item):
        pass

    def next(self):
        pass

    def play(self, item):
        self.index += 1
        if isinstance(item, models.Review):
            word = item.word
        elif isinstance(item, models.Word):
            word = item
        sys.stdout.write(styles.RANDOM(self.short_name.upper(), length=False))
        sys.stdout.write(" ")
        phon = functions.play_word(word, self.index)
        if not hasattr(styles, phon.type.content):
            sys.stdout.write(phon.type.content)
        elif not callable(getattr(styles, phon.type.content)):
            sys.stdout.write(phon.type.content)
        else:
            func = getattr(styles, phon.type.content)
            sys.stdout.write(func(phon.type.content))
        sys.stdout.write(" ")
        if " " in word.title:
            sys.stdout.write(styles.PHRASE("PHRASE"))
        else:
            sys.stdout.write(styles.SINGLE("SINGLE"))

    def print_paras(self, word):
        print(settings.SPLITTER)
        functions.print_paras(word)
        print(settings.SPLITTER)

    def practice(self, word):
        functions.prints(word)
        title = word.title
        while True:
            var = functions.input()[0]
            if not var:
                continue
            if title.lower() == var.lower():
                break
            print(styles.ERROR(var, True))

    @transaction.atomic
    def study_one(self, item):
        if isinstance(item, models.Review):
            word = item.word
        elif isinstance(item, models.Word):
            word = item
        dandan.system.clear()
        self.play(word)
        titles = functions.input(" ")

        action = titles[0]
        if not action:
            return status.PLAY
        if action in {'e', 'exit'}:
            return status.EXIT
        if action in {'n', }:
            return status.SKIP
        if action in {'para', 'p', "trans", "t"}:
            self.print_paras(word)
            functions.getch()
            return status.PARA

        print(settings.SPLITTER)

        data = study.check(word, titles)

        for item in data.list:
            if item.error:
                print(styles.ERROR(item.title, True))
                continue
            if item.equal:
                print(styles.EQUAL(item.title, True))
                self.print_paras(word)
                continue
            if item.right:
                print(styles.RIGHT(item.title, True))
                self.print_paras(word)
                continue
            if item.exists:
                print(styles.EXIST(item.title, True))
                self.print_paras(functions.get_word(item.title))

        if data.error:
            self.practice(word)
            return status.ERROR
        return status.RIGHT

    def study(self,):
        item = None
        while True:
            if not item:
                item = self.next()
            if not item:
                break
            command = self.study_one(item)
            if command == status.PLAY:
                continue
            if command == status.PARA:
                self.para(item)
                continue
            if command == status.EXIT:
                exit(0)
            if command == status.SKIP:
                self.skip(item)
                item = None
                continue
            if command == status.RIGHT:
                self.right(item)
                item = None
                functions.getch()
                continue
            if command == status.ERROR:
                self.error(item)
                pass


class PracticeMethod(DictationMethod):

    name = "practice"
    short_name = "p"
    help = "Practice word in schedule"

    def __init__(self):

        if not study.has_practice():
            print(styles.SUCCESS("No any word can to practice"))

    def next(self):

        return study.get_random_practice()

    def right(self, word):
        key = functions.getch()
        if key == "r":
            models.Review.objects.get_or_create(word=word)
            print(styles.SUCCESS("Save to review success!!!"))


class HardMethod(DictationMethod):

    name = "hard"
    short_name = "h"
    help = "Practice hard word in schedule"

    def __init__(self):
        if not study.has_hard():
            near = study.get_near_hard()
            delta = near.review_time - timezone.now()
            print(styles.SUCCESS("Next hard after {}".format(delta)))

    def next(self):
        return study.get_random_hard()

    def right(self, item):
        study.hard_right(item.word)

    def error(self, item):
        study.hard_error(item.word)


class ReviewMethod(DictationMethod):

    name = "review"
    short_name = "r"
    help = "Review word in schedule"

    def __init__(self):
        if not study.has_review():
            near = study.get_near_review()
            delta = near.review_time - timezone.now()
            print(styles.SUCCESS("Next review after {}".format(delta)))

    def next(self):
        return study.get_random_review()

    def right(self, item):
        study.review_right(item.word)

    def error(self, item):
        study.review_error(item.word)


class Command(BaseCommand):
    help = 'Review word in database'

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.actions = {
            "help": "show help information",
            ReviewMethod.name: [ReviewMethod, ],
            PracticeMethod.name: [PracticeMethod, ],
            HardMethod.name: [HardMethod, ],
            "dictation": [HardMethod, ReviewMethod],
        }

    def man(self):
        for var in self.actions:
            if hasattr(self.actions[var], "help"):
                help = self.actions[var].help
            else:
                help = self.actions[var]
            print("{} : {}".format(var, help))

    def add_arguments(self, parser):
        help = ", ".join(self.actions.keys())
        parser.add_argument('method', nargs=1, type=str, help=help)

    def handle(self, *args, **options):
        functions.show_console_log(False)
        method = options["method"][0]
        if method not in self.actions:
            print(self.style.WARNING("No such method {}".format(method)))
            return
        if method == "help":
            self.man()
            return
        methods = self.actions[method]
        for method in methods:
            self.method = method()
            self.method.study()
