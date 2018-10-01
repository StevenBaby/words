# coding=utf-8
from __future__ import print_function, unicode_literals
import dandan
import refine

api = "http://word.iciba.com/"


def load(name):
    filename = "{}.json".format(name)
    data = dandan.value.get_json(filename)
    if data:
        return data
    return []


def save(data, name):
    filename = "{}.json".format(name)
    dandan.value.put_json(data, filename)


def get_page(data, course, page):
    print("get {} {}".format(course, page))
    params = {
        "action": "words",
        "class": course,
        "course": page,
    }
    soup = dandan.query.soup(api, params=params)
    spans = soup.select("ul.word_main_list > li > div.word_main_list_w > span")
    for span in spans:
        title = span.attrs.get("title").strip()
        if not refine.valid(title):
            continue
        if title in data:
            continue
        data.append(title)


def get_course(course, name):
    data = load(name)
    params = {
        "action": "courses",
        "classid": course,
    }
    soup = dandan.query.soup(api, params=params)
    lis = soup.select("li")
    for li in lis:
        page = li.attrs.get("course_id")
        get_page(data, course, page)
        # save(data)
    save(data, name)
    return data


if __name__ == '__main__':
    print(get_course(717, name="三级笔译(下)"))
