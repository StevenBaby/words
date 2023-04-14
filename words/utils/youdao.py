# encoding=utf-8
from __future__ import print_function, unicode_literals, division
import re
import os
import six
import dandan
import requests

session = requests.Session()
session.trust_env = False

PHONETIC_UK = 1
PHONETIC_US = 2

CONTENT_UK = 'UK'
CONTENT_US = 'US'

PHONETICS = {
    PHONETIC_UK: CONTENT_UK,
    PHONETIC_US: CONTENT_US,
}

SEARCH_API = "http://www.youdao.com/w/eng/{title}/"
PHONETIC_API = "http://dict.youdao.com/dictvoice"
TRANS_API = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

PARA_TYPES = {"none", "adj", "adv", "aux", "n", "pron", "v", "vt", "vi", "num", "art", "prep", "conj", "int", "abbr", }


def get_keyword(content):
    keyword = content.select_one(".keyword")
    if not keyword:
        return None
    match = re.match(r"^[-\w ]+$", keyword.get_text().strip())
    if not match:
        return None
    return match.group(0)


def get_phonetics(content):
    phonetics = []
    phons = content.select(".pronounce")
    for phon in phons:
        phonstring = phon.select_one(".phonetic")
        if not phonstring:
            phonstring = " "
        else:
            phonstring = phonstring.get_text().strip()

        if "英" in phon.get_text():
            value = dandan.value.AttrDict()
            value.content = phonstring
            value.type = PHONETIC_UK
            value.description = CONTENT_UK
            phonetics.append(value)
        elif "美" in phon.get_text():
            value = dandan.value.AttrDict()
            value.content = phonstring
            value.type = PHONETIC_US
            value.description = CONTENT_US
            phonetics.append(value)

    return phonetics


def get_paras(soup):
    result = []
    content = soup.select_one("#phrsListTab")
    if not content:
        return []
    paras = content.select("li")

    for para in paras:
        line = para.get_text().strip()
        tup = line.split(".", 1)
        if tup[0] not in PARA_TYPES:
            cla = "none"
            content_line = line
        else:
            cla = tup[0]
            content_line = tup[1]
        contents = re.split(r'[；，。;,]', content_line)
        contents = [var.strip() for var in contents if var.strip()]
        for content in contents:
            if not content:
                continue
            para = dandan.value.AttrDict()
            para.type = cla
            para.content = content
            result.append(para)
    return result


def get_webphrases(soup):
    keyword = soup.select_one('.keyword')
    if not keyword:
        return []
    keyword = keyword.get_text().strip()

    content = soup.select_one("#webPhrase")
    if not content:
        return []
    for group in content.select(".wordGroup"):
        title = group.select_one(".contentTitle")
        if not title:
            continue
        title = title.get_text().strip()
        if title != keyword:
            continue

        para = dandan.value.AttrDict()
        para.type = 'none'
        para.content = group.get_text().replace(title, '').strip()
        return [para, ]


def get_webparas(soup):
    content = soup.select_one("#webTrans")
    if not content:
        return []
    container = content.select_one(".wt-container")
    if not container:
        return []

    title = container.select_one('.title')
    if not title:
        return []

    para = dandan.value.AttrDict()
    para.type = 'none'
    para.content = title.get_text().strip()
    return [para, ]


def get_ydparas(soup):
    content = soup.select_one("#ydTrans")
    if not content:
        return []
    container = content.select_one(".trans-container")
    if not container:
        return []

    trans = container.select('p')
    if len(trans) < 2:
        return []

    para = dandan.value.AttrDict()
    para.type = 'none'
    para.content = trans[1].get_text().strip()
    return [para, ]


def get_paraphrases(word):
    result = {}
    for para in word.paras:
        result.setdefault(para.type, [])
        result[para.type].append(para.content)
    for type in result.keys():
        result[type] = "，".join(result[type])
    return [[var[0], var[1]] for var in result.items()]


def get_ranks(soup):
    # rank
    result = []
    ranks = soup.select_one(".via.rank")
    if not ranks:
        return result
    if not ranks.get_text():
        return result
    for rank in ranks.get_text().split(" "):
        if not rank.strip():
            continue
        result.append(rank.strip())
    return result


def get_star(soup):
    # star
    result = 0
    star = soup.select_one(".star")
    if not star:
        return result

    clas = star.attrs.get("class")
    for cla in clas:
        match = re.match(r"star(\d+)", cla)
        if not match:
            continue
        result = int(match.group(1))
    return result


def get_synonyms(soup):
    result = []
    synonyms = soup.select_one("#synonyms")
    if not synonyms:
        return []
    for a in synonyms.select("a"):
        syn = a.get_text().strip()
        result.append(syn)
    return result


def get_phrases(soup):
    phrases = []
    group = soup.select_one("#wordGroup")
    if not group:
        return phrases
    for phrase in group.select(".contentTitle"):
        phrase = phrase.get_text().strip()
        phrases.append(phrase)
    return phrases


def get_sentences(soup):
    # sentence
    sentences = []
    sentence = soup.select_one("#examplesToggle")
    if not sentence:
        return sentences

    lis = sentence.select("li")
    for li in lis:
        p = li.select_one("p")
        if not p:
            continue
        sentences.append(p.get_text().strip())
    return sentences


def get_word(title):
    '''
    Get youdao word paraphrase

    Args:
        * title (string): word title

    Returns:
        * dandan.value.AttrDict: word
    '''
    url = SEARCH_API.format(title=title)
    # params = {"q": title}
    soup = dandan.query.soup(url=url, timeout=3, retry=2)

    word = dandan.value.AttrDict()
    word.title = title
    word.type = "EN"
    word.paras = get_paras(soup) or get_webphrases(soup) or get_webparas(soup) or get_ydparas(soup)

    word.phonetics = get_phonetics(soup)
    word.ranks = get_ranks(soup)
    word.star = get_star(soup)
    word.synonyms = get_synonyms(soup)
    word.phrases = get_phrases(soup)
    word.sentences = get_sentences(soup)

    if not word.paras:
        return None
    word.paraphrases = get_paraphrases(word)
    title = get_keyword(soup)
    if title:
        word.title = title

    return word


def get_phonetic_url(title, type=PHONETIC_UK):
    from requests import Request
    if isinstance(type, six.string_types):
        if type == CONTENT_US:
            type = PHONETIC_US
        elif type == CONTENT_UK:
            type = PHONETIC_UK
        else:
            type = 0
    if type not in PHONETICS:
        type = PHONETIC_UK

    params = {
        "audio": title,
        'type': type,
    }
    request = Request("get", PHONETIC_API, params=params).prepare()
    return request.url


def get_phonetic(title, filename, type=PHONETIC_UK):
    '''
    Get word phonetic title save to filename

    Args:
        * title (string): title of word
        * filename (stirng): local system filename
        * type (string, optional): must be in definite as PHONETIC_UK or PHONETIC_US

    Raises:
        * OSError: if filename cannot write
    '''
    filename = os.path.abspath(filename)
    if not dandan.system.writeable(filename):
        raise OSError("File {} unwriteable".format(filename))
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    url = get_phonetic_url(title=title, type=type)
    dandan.traffic.download(url, filename)


def main():
    # word = get_word('hello')
    # print(word)
    # word = get_word('I like to eat pizza')
    # print(word)
    word = get_word("The car won't start")
    print(word)


if __name__ == '__main__':
    main()
