# encoding=utf-8
from __future__ import print_function, unicode_literals, division
from django.core.management.base import BaseCommand

# import six
import logging
import dandan
from words import functions
from words import models
from utils import youdao

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Operate word in database'

    def operate_review(self, word):
        if word.review.first():
            functions.getch()
            return
        action = functions.input(self.style.WARNING("Save to review (yes)?"))[0]
        if action not in ("yes", "YES", "y", "Y"):
            return
        functions.set_review(word)
        print(self.style.SUCCESS("Save to review success."))
        functions.getch()

    def operate_word(self, word):
        functions.prints(word)
        self.operate_review(word)

    def operate_result(self, title):
        result = youdao.get_word(title)
        if not result:
            print("Search not found '{}'".format(title))
            functions.getch()
            return
        functions.prints(result)
        action = functions.input(self.style.WARNING("Save to dictionary (yes)?"))[0]
        if action not in ("yes", "YES", "y", "Y"):
            return
        word = functions.save(result)
        if word:
            print(self.style.SUCCESS("Save to dictionary success."))
            self.operate_review(word)
        else:
            print(self.style.ERROR("Save to dictionary failure."))
            functions.getch()

    def operate(self):
        dandan.system.clear()
        title = functions.input(self.style.WARNING("title:"))[0]
        if title in ("e", "exit"):
            exit(0)
        if not title:
            return

        if not functions.exists(title):
            self.operate_result(title)
            return

        word = models.Word.objects.filter(title=title).first()
        self.operate_word(word)
        return

    def handle(self, *args, **options):
        functions.show_console_log(False)
        while True:
            self.operate()
