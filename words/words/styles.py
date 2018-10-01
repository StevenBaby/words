# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import colorama
import dandan
import unicodedata


def LENGTH(string):
    from django.conf import settings
    delta = len(settings.SPLITTER) - dandan.value.length(string)
    if delta <= 0:
        return string
    style = "{: ^%d}" % (len(string) + delta)
    string = style.format(string)
    return string


def ERROR(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.RED,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def EQUAL(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.GREEN,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def RIGHT(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.CYAN,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def EXIST(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.YELLOW,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def SUCCESS(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.GREEN,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def WARNING(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.YELLOW,
        colorama.Fore.BLACK,
        string,
        colorama.Style.RESET_ALL,
    )


def SINGLE(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.CYAN,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def PHRASE(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.MAGENTA,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def UK(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.CYAN,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def US(string, length=False):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.MAGENTA,
        colorama.Fore.WHITE,
        string,
        colorama.Style.RESET_ALL,
    )


def TITLE(string, length=True):
    if length:
        string = LENGTH(string)
    return "{}{}{}{}".format(
        colorama.Back.WHITE,
        colorama.Fore.MAGENTA,
        string,
        colorama.Style.RESET_ALL,
    )


def RANDOM(string, length=False):
    import inspect
    import random
    import re
    module = inspect.getmodule(inspect.currentframe())
    ignores = {
        "RANDOM",
        "LENGTH",
    }
    funcs = []
    for name in dir(module):
        if name in ignores:
            continue
        attr = getattr(module, name)
        if not callable(attr):
            continue
        match = re.match("[A-Z]+", name)
        if not match:
            continue

        funcs.append(attr)
    return random.choice(funcs)(string, length)
