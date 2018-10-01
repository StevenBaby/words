from __future__ import print_function, unicode_literals, absolute_import
import os
import glob
import dandan
import re
import sys


dirname = os.path.dirname(os.path.abspath(__file__))
project = os.path.dirname(dirname)
if project not in sys.path:
    sys.path.insert(0, project)


def valid(title):
    if dandan.value.length(title) < 2:
        return False
    match = re.search(r"[-'\[\]\.)(\*/’!]", title)
    if match:
        return False
    ignores = {'exit', }
    if title in ignores:
        return False

    return True


def refine(title):
    new_title = re.sub(r" +", " ", title)

    if new_title != title:
        print("revine [{}] to [{}]".format(title, new_title))
        title = new_title

    # from words import models
    # if models.Word.objects.filter(title=title).exists():
    #     return title

    # word = models.Word.objects.filter(title__iexact=title).first()
    # if word:
    #     print("revine [{}] to [{}]".format(title, word.title))
    #     return word.title

    # return None

    # from utils import youdao

    # print("Get word {}".format(title))
    # word = youdao.get_word(title)
    # if not word:
    #     return None

    # for para in word.paras:
    #     content = para.content
    #     match = re.search(r"子名|人名|女名|男名|名字|（", content)
    #     if match:
    #         print("word {} paras {}".format(title, content))
    #         print(title, content)
    #         return None

    # print("word {} paras {}".format(title, content))

    return title


def refine_item(filename):
    data = dandan.value.get_json(filename)
    if not data:
        return
    if not isinstance(data, list):
        return

    res = {}
    for title in data:
        if not valid(title):
            print("Invalide  [{}]".format(title))
            continue
        new_title = refine(title)
        if not new_title:
            print("Ignore [{}]".format(title))
            continue
        res[new_title] = True
    dandan.value.put_json(list(res.keys()), filename, indent=4)


def refine_dir(dirname):
    files = glob.glob(os.path.join(dirname, "*"))
    for filename in files:
        if os.path.isfile(filename) and filename.endswith(".json"):
            refine_item(filename)
            continue
        if os.path.isdir(filename):
            refine_dir(filename)


def main():
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
    django.setup()
    refine_item("轻松背单词/分级单词/第04级.json")

    # dirname = os.path.dirname(os.path.abspath(__file__))
    # refine_dir(dirname)


if __name__ == '__main__':
    main()
