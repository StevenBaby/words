# -*- coding:utf-8 -*-
import logging

from django.utils import timezone
from django import template
from django.utils.translation import ugettext_lazy as _

from words import functions
from words import statistics
from words import study


import resources

logger = logging.getLogger("words")

register = template.Library()


@register.simple_tag(takes_context=True, name="get_review")
def get_review(context, word):
    user = context.get("user", None)
    if not user:
        return
    return functions.get_review(user=user, word=word)


@register.simple_tag(takes_context=True, name="get_word")
def get_word(context, title):

    return functions.get_word(title=title)


@register.simple_tag(takes_context=True, name="get_study_count")
def get_study_count(context, type):
    user = context.get("user", None)
    if not user:
        return 0
    if type == "review":
        return study.get_review_count(user=user)
    elif type == "hard":
        return study.get_hard_count(user=user)
    elif type == "practice":
        words = context.request.session.get("practice", [])
        return len(words) or study.get_practice_count(user=user)
    elif type == "founding":
        return len(context.request.session.get("practice", []))
    elif type == 'study':
        return study.get_review_count(user=user) + study.get_hard_count(user=user)
    return 0


@register.simple_tag(takes_context=True, name="get_study_color")
def get_study_color(context, type):
    count = get_study_count(context, type)
    if count < 1:
        return "green"
    if count < 20:
        return "blue"
    if count < 50:
        return "yellow"
    if count < 100:
        return "orange"
    else:
        return "red"


@register.simple_tag(name="get_phonetic_content")
def get_phonetic_content(word, type):
    return functions.get_phonetic_content(word, type)


@register.simple_tag(name="get_phonetic_color")
def get_phonetic_color(type):
    if type == "UK":
        return "blue"
    if type == "US":
        return "teal"
    return ""


@register.simple_tag(name="get_phonetic_title")
def get_phonetic_title(type):
    if type == "UK":
        return _("UK")
    if type == "US":
        return _("US")
    return ""


@register.simple_tag(takes_context=True, name="get_level_count")
def get_level_count(context):
    user = context.get("user", None)
    if not user:
        return []
    return statistics.get_level_count(user=user)


@register.simple_tag(takes_context=True, name="get_resources")
def get_resources(context):
    res = resources.get_resources()
    return res


@register.simple_tag(name="get_date_count")
def get_date_count(date=None):
    return statistics.get_date_count(date)
