#!/usr/bin/python
# coding=utf-8
from __future__ import print_function, unicode_literals
import os
import re
import sys
import traceback
import socket
import logging
import logging.config
from distutils.version import StrictVersion


if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("utf8")


dirname = os.path.dirname(os.path.abspath(__file__))

base_dir = os.path.dirname(dirname)

manage = os.path.join(base_dir, "manage.py")

logger = logging.getLogger("words")

host = "127.0.0.1"
port = 8888


def get_logger():

    log_path = os.path.join(base_dir, "local", "log")
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file = os.path.join(log_path, "starter.log")

    config = {
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] [%(module)s] [%(lineno)d] [%(levelname)s] | %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                "level": "DEBUG",
            },
            'null': {
                'class': 'logging.NullHandler',
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'verbose',
                'filename': log_file,
                'when': "MIDNIGHT",
                "level": "INFO",
                "backupCount": 5,
            },
        },
        'loggers': {
            'starter': {
                'handlers': ['console', "file", ],
                'level': "DEBUG",
                'propagate': True,
            },
        },
    }

    logging.config.dictConfig(config)
    return logging.getLogger("starter")


def requirements():
    requirefile = os.path.join(os.path.dirname(dirname), "requirements.txt")
    if not os.path.exists(requirefile):
        logger.fatal("can not found requirements.txt")
        return
    for line in open(requirefile):
        line = line.strip()
        if line.startswith("#"):
            continue
        tup = re.split("[<>=]", line)
        lib = tup[0]
        version = "0.0.0"
        if len(tup) == 2:
            version = tup[1]
        try:
            module = __import__(lib)
            if StrictVersion(version) <= StrictVersion(module.__version__):
                continue
            raise Exception()
        except Exception:
            command = '''pip install --upgrade "{}" -i https://pypi.tuna.tsinghua.edu.cn/simple'''.format(line)
            logger.info(command)
            os.system(command)

        try:
            module = __import__(lib)
            if StrictVersion(version) <= StrictVersion(module.__version__):
                continue
            raise Exception()
        except Exception:
            logger.fatal("Cannot install library %s, please try again later.", lib)
            exit(0)


def migrate():
    import dandan
    command = "python {} makemigrations".format(manage)
    logger.info(command)

    results, code = dandan.system.execute(command)
    logger.info(results)

    command = "python {} migrate".format(manage)
    logger.info(command)

    results, code = dandan.system.execute(command)
    logger.info(results)


def get_run_command():
    run_command = "python {script} runserver {host}:{port} --noreload --insecure".format(
        script=manage,
        host=host,
        port=port,
    )
    return run_command


def stop():
    import dandan
    if dandan.system.is_linux():
        command = '''ps -ef | grep "{}" | grep -v grep'''.format(get_run_command())
        results, code = dandan.system.execute(command)
        logger.info(results)

        results = results.splitlines()

        for result in results:
            match = re.search(r"\w+ +(\d+) +\d+", result)
            if not match:
                continue
            pid = match.group(1)
            command = "kill -9 {}".format(pid)
            logger.info(command)
            os.system(command)
    elif dandan.system.is_win32():
        run_para = get_run_command().strip("python").strip()
        command = '''wmic process where caption="python.exe" get commandline,processid'''

        results, code = dandan.system.execute(command)
        logger.info(results)

        results = results.splitlines()
        for result in results:
            match = re.search(r"python +(?P<para>.+) +(?P<pid>\d+)", result)
            if not match:
                continue
            para = match.group("para").strip()
            if para != run_para:
                continue
            pid = match.group("pid")
            command = "taskkill /F /PID {}".format(pid)
            logger.info(command)
            os.system(command)
    else:
        logger.fatal("Sorry, this platform %s not supported, exit...", sys.platform)
        exit(0)


def start():
    command = get_run_command()
    logger.info(command)
    try:
        return os.system(command)
    except KeyboardInterrupt:
        return 0


def is_runing():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
        return True
    except Exception as e:
        return False


def run():
    logger.info("start words server")
    if is_runing():
        logger.info("server already running")
        return False
    requirements()
    migrate()
    stop()
    code = start()
    if code == 0:
        return False
    else:
        return True


def main():
    global logger
    logger = get_logger()
    try:
        while run():
            pass
    except Exception:
        logger.fatal(traceback.format_exc())


if __name__ == '__main__':
    main()
