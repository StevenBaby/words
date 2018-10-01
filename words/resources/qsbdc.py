# coding=utf-8
from __future__ import print_function, unicode_literals

# import six
import dandan
import refine


data = []


def get_page(url, level, page):
    print("get {} {} {}".format(url, level, page))
    global data
    params = dandan.value.AttrDict()
    params.level = level
    params.page_id = page
    soup = dandan.query.soup(url, params=params)
    spans = soup.select("span.hidden_1_1")
    for span in spans:
        title = span.get_text().strip()
        if not refine.valid(title):
            continue
        if title in data:
            continue
        data.append(title)


def get_level(url, level):
    global data
    data = []
    params = dandan.value.AttrDict()
    params.level = level
    soup = dandan.query.soup(url, params=params)
    options = soup.select("td > select > option")
    for option in options:
        page = option.attrs.get('value')
        get_page(url, level, page)

    name = "第{}级.json".format(level)
    dandan.value.put_json(data, name)


def main():
    # url = 'http://word.qsbdc.com/wl.php'
    url = 'http://phrase.qsbdc.com/wl.php'
    for var in range(3, 11):
        get_level(url, var)
        # break


if __name__ == '__main__':
    main()
