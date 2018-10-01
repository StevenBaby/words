# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import re
import six
import dandan


def recent():
    result = dandan.value.AttrDict()

    url = "http://www.51voa.com/"
    soup = dandan.query.soup(url)

    item = soup.select_one("#right_box #list li")
    if not item:
        return None

    aa = item.select("a")
    if not aa:
        return None

    if len(aa) < 2:
        return None

    result.category = aa[0].get_text().strip("[").strip("]").strip()

    match = re.match(r"(?P<title>.+)\((?P<date>.+)\)", aa[-1].get_text())
    if not match:
        return None

    result.title = match.group("title").strip()
    result.date = match.group("date").strip()

    content_url = six.moves.urllib.parse.urljoin(url, aa[-1].attrs.get("href"))

    soup = dandan.query.soup(content_url)

    contents = soup.select("#content p")
    if not contents:
        return None

    result.contents = [] 
    for content in contents:
        result.contents.append(content.get_text().strip())

    mp3 = soup.select_one("#menubar #mp3")
    if not mp3:
        return result

    result.mp3 = mp3.attrs.get("href")

    lrc = soup.select_one("#menubar #lrc")
    if not lrc:
        return result

    result.lrc = lrc.attrs.get("href")

    return result


if __name__ == '__main__':
    print(recent())
