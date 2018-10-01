#!/usr/bin/python3
# coding=utf-8
from __future__ import print_function, unicode_literals

import re
import os
import sys
import glob
import shutil
import dandan
from distutils.version import StrictVersion

currentname = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(currentname))

source_dir = os.path.join(os.path.dirname(dirname), "words")

if source_dir not in sys.path:
    sys.path.insert(0, source_dir)

import words

direct_dir = os.path.join(dirname, "build_{}".format(words.__version__))

ignores = {
    os.path.join(source_dir, "local"),
    os.path.join(source_dir, "resources", "crawler.py"),
    os.path.join(source_dir, "resources", "qsbdc.py"),
    os.path.join(source_dir, "resources", "refine.py"),
    os.path.join(source_dir, "words", "management"),
}


additions = {
    os.path.join(dirname, "build", "start.cmd"),
}

migrations = {
    "__init__.py",
    "0001_initial.py"
}


def glob_dir(dirname, *basenames):
    print("in to directory {}".format(dirname))
    basenames = list(basenames)
    files = glob.glob(os.path.join(dirname, "*"))
    for filename in files:
        if filename in ignores:
            continue
        if filename.endswith(".pyc"):
            continue
        basename = os.path.basename(filename)
        if basename == "__pycache__":
            continue
        # if dirname.endswith("migrations") and basename not in migrations:
        #     continue

        basenames.append(basename)
        if os.path.isfile(filename):
            newfilename = os.path.join(direct_dir, *basenames)
            if not os.path.exists(os.path.dirname(newfilename)):
                os.makedirs(os.path.dirname(newfilename))
            print("copy filename {} to {}".format(filename, newfilename))
            shutil.copy2(filename, newfilename)
        elif os.path.isdir(filename):
            glob_dir(filename, *basenames)
        basenames = basenames[:-1]


def glob_additions():
    for filename in additions:
        basename = os.path.basename(filename)
        newfilename = os.path.join(direct_dir, basename)
        if not os.path.exists(os.path.dirname(newfilename)):
            os.makedirs(os.path.dirname(newfilename))
        print("copy filename {} to {}".format(filename, newfilename))
        shutil.copy2(filename, newfilename)


def zip_build():
    import zipfile
    resultname = direct_dir + ".zip"
    resultfile = zipfile.ZipFile(resultname, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(direct_dir):
        for filename in filenames:
            sourcefile = os.path.join(dirpath, filename)
            directfile = sourcefile.replace(dirname, "")
            print("zip file {} to {}".format(sourcefile, directfile))
            resultfile.write(sourcefile, directfile)
    resultfile.close()

    print("wait for copy latest.zip")

    latest_file = os.path.join(dirname, "latest.zip")
    shutil.copy2(resultname, latest_file)

    print("wait for delete {}".format(direct_dir))
    shutil.rmtree(direct_dir)


def refresh_python_in_readme():

    pythons = {
        "version": StrictVersion("3.6.3"),
        "x64": "https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe",
        "x86": "https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe"
    }

    pythons = dandan.value.AttrDict(pythons)

    url = 'https://www.python.org/downloads/release'
    print("get url {}".format(url))
    soup = dandan.query.soup(url)

    aa = soup.select(".release-number > a")
    version = StrictVersion("0.0.0")
    url = ""
    for a in aa:
        text = a.get_text().strip()
        if not text:
            continue
        try:
            ver = StrictVersion(text.split(" ")[-1])
        except Exception:
            continue
        if ver > version:
            version = ver
            url = a.attrs.get("href")
    if not url:
        return

    pythons.version = version

    url = "https://www.python.org" + url
    print("get url {}".format(url))
    soup = dandan.query.soup(url)

    aa = soup.select("tr > td > a")

    for a in aa:
        text = a.get_text().strip()
        if text == "Windows x86-64 executable installer":
            pythons.x64 = a.attrs.get("href")
            continue
        if text == "Windows x86 executable installer":
            pythons.x86 = a.attrs.get("href")
            continue

    filename = os.path.join(os.path.dirname(dirname), "README.md")
    lines = []

    for line in open(filename, encoding="utf-8"):
        match = re.search(r"\[点击下载 Python .+ Windows (?P<platform>.+)\]\(.+\)", line)
        if not match:
            lines.append(line)
            continue
        platform = match.group("platform")
        line = "    - [点击下载 Python {} Windows {}]({})\n".format(pythons.version, platform, pythons[platform])
        lines.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)


if __name__ == '__main__':
    glob_dir(source_dir)
    glob_additions()
    zip_build()
    # refresh_python_in_readme()
