# -*- coding:utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_info
from django.conf import settings

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

from distutils.version import StrictVersion

import six
import random
import logging
import dandan
import words


logger = logging.getLogger("words")

register = template.Library()

LANGUAGES = {}
for code, name in settings.LANGUAGES:
    LANGUAGES[code] = get_language_info(code)
    LANGUAGES[code]["flag"] = ""
    if code == "zh-hans":
        LANGUAGES[code]["flag"] = "cn"
    elif code == "en-us":
        LANGUAGES[code]["flag"] = "us"


@register.simple_tag(name="base_languages")
def base_languages(current_code):
    if not current_code:
        current_code = settings.LANGUAGE_CODE
    if current_code not in LANGUAGES:
        current = LANGUAGES[settings.LANGUAGE_CODE]
    else:
        current = LANGUAGES[current_code]
    return {'languages': LANGUAGES, 'current': current}


@register.simple_tag(name="base_info")
def base_info():
    return {
        "current_time": timezone.localtime(),
        "project_name": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
        "version": StrictVersion(words.__version__),
    }


@register.simple_tag(name="random_color")
def random_color():
    color = random.choice(["red", "orange", "yellow", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown"])
    return color


@register.simple_tag(takes_context=True, name="set")
def set(context, key, value):
    """
    Sets a value to the global template context, so it can
    be accessible across blocks.

    Note that the block where the global context variable is set must appear
    before the other blocks using the variable IN THE BASE TEMPLATE.  The order
    of the blocks in the extending template is not important.

    Usage::
        {% extends 'base.html' %}

        {% block first %}
            {% set_global_context 'foo' 'bar' %}
        {% endblock %}

        {% block second %}
            {{ foo }}
        {% endblock %}
    """
    context.dicts[0][key] = value
    return ""


@register.simple_tag(name="add")
def add(a, b):
    return a + b


@register.filter()
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))


@register.simple_tag(takes_context=True, name="paginator")
def paginator(context, items, page=1, page_size=12):
    paginator = Paginator(items, page_size)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag(name='timedelta')
def timedelta(delta=None):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    if not delta:
        return ""
    remain = int(delta.total_seconds())

    remain, seconds = divmod(remain, 60)
    remain, minutes = divmod(remain, 60)
    days, hours = divmod(remain, 24)

    # result = "{:0>2}:{:0>2}:{:0>2}".format(hours, minutes, seconds)
    # if days > 0:
    #     result = "{} {} ".format(days, _("days")) + result
    result = dandan.value.AttrDict()
    result.days = days
    result.hours = "{:0>2}".format(hours)
    result.minutes = "{:0>2}".format(minutes)
    result.seconds = "{:0>2}".format(seconds)
    return result.dict()


@register.simple_tag(takes_context=True, name='fitpage')
def fitpage(context, value, name='page'):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    request = context.get("request", None)
    if not request:
        return "?name={}".format(value)

    path = request.get_full_path()
    res = six.moves.urllib.parse.urlparse(path)
    query = dict([(k, v[0]) for k, v in six.moves.urllib.parse.parse_qs(res.query).items()])
    query[name] = value
    if name != "page":
        query["page"] = 1
    querys = ["=".join([str(var[0]), str(var[1])]) for var in query.items()]
    querys = "&".join(querys)
    return "{}?{}".format(res.path, querys)


@register.simple_tag(name='get_type')
def get_type(object):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    return type(object).__name__


@register.simple_tag(name='has_superuser')
def has_superuser():
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    exists = User.objects.filter(id=1).exists()
    # logger.debug("super user exists %s", exists)
    return exists
