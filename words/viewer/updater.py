# coding=utf-8
from __future__ import print_function, unicode_literals
import os
import dandan
import logging
import six
import zipfile
import glob
import shutil
from django.conf import settings as djsettings
from distutils.version import StrictVersion

from viewer import starter
import words


logger = logging.getLogger("words")
settings = None


def get_file_version(filename):
    if not filename.endswith(".zip"):
        return None
    if filename == 'latest.zip':
        return None
    if not filename.startswith("build_"):
        return None

    version = filename.replace(".zip", "").replace("build_", "")
    return StrictVersion(version)


def get_lastest():

    url = 'https://github.com/StevenKjp/words/tree/master/build'
    soup = dandan.query.soup(url)
    trs = soup.select("tr.js-navigation-item")
    version = StrictVersion(words.__version__)
    reason = ""

    for tr in trs:
        span = tr.select_one("td.content > span")
        if not span:
            continue
        filename = span.get_text()
        ver = get_file_version(filename)
        if not ver:
            continue
        if ver < version:
            continue
        version = ver
        reason = ""
        message = tr.select_one("td.message > span")
        if not message:
            continue
        reason = message.get_text()


    latest = dandan.value.AttrDict()
    latest.version = version
    latest.reason = reason

    return latest


def extract(filename, direct):
    global settings
    settings.updater.status = 'updating'
    settings.updater.updating.status = 'extracting'

    zfile = zipfile.ZipFile(filename, 'r')

    settings.updater.updating.total = len(zfile.namelist())
    for var in six.moves.range(0, settings.updater.updating.total):

        settings.updater.updating.value = var

        path = zfile.namelist()[var]
        result = os.path.join(direct, path.split("/", 1)[1])
        dirname = os.path.dirname(result)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        logger.info("extract file {} to {}".format(path, result))
        with open(result, 'wb') as file:
            file.write(zfile.read(path))


def callback(value, total, time):
    global settings
    settings.updater.status = "updating"
    settings.updater.updating.status = "downloading"
    settings.updater.updating.total = total
    settings.updater.updating.value = value
    # logger.debug(settings.updater.updating)


def update(json_settings):
    global settings
    settings = json_settings

    settings.updater.status = "updating"
    settings.updater.updating.status = "downloading"

    latest_url = 'https://github.com/StevenKjp/words/raw/master/build/latest.zip'
    filename = os.path.join(djsettings.DATABASE_DIR, "latest.zip")
    if os.path.exists(filename):
        os.remove(filename)
    logger.info("start download latest.zip from {} to {}".format(latest_url, filename))
    dandan.traffic.download(url=latest_url, filename=filename, callback=callback)

    updatepath = os.path.join(djsettings.DATABASE_DIR, "update")
    if os.path.exists(updatepath):
        shutil.rmtree(updatepath, ignore_errors=True)

    currentpath = os.path.join(updatepath, "current")

    extract(filename, currentpath)
    oldpath = os.path.join(updatepath, "old")
    if not os.path.exists(oldpath):
        os.makedirs(oldpath)

    settings.updater.status = "updating"
    settings.updater.updating.status = "moving"
    settings.updater.updating.total = 1
    settings.updater.updating.value = 1

    oldfiles = glob.glob(os.path.join(djsettings.BASE_DIR, '*'))
    for filename in oldfiles:
        basename = os.path.basename(filename)
        if basename == 'local':
            continue
        logger.info("move file {} to {}".format(filename, oldpath))
        shutil.move(filename, oldpath)

    newfiles = glob.glob(os.path.join(currentpath, '*'))
    for filename in newfiles:
        logger.info("move file {} to {}".format(filename, djsettings.BASE_DIR))
        shutil.move(filename, djsettings.BASE_DIR)

    settings.updater.status = "updating"
    settings.updater.updating.status = "finished"
    settings.updater.updating.total = 1
    settings.updater.updating.value = 1

    starter.stop()

    logger.info("update finished.")
