# encoding=utf-8
from __future__ import print_function, unicode_literals, division

import os
import sys
import re

from django.core.management.base import BaseCommand
from django.conf import settings

import dandan
import logging

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Run server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action', '-a',
            type=str,
            required=True,
            help="action type",
            choices=['start', 'stop', 'restart', 'back', ])

    def handle(self, *args, **options):
        action = options["action"]
        getattr(self, action)()

    def get_run_command(self):
        manage = os.path.join(settings.BASE_DIR, 'manage.py')
        run_command = "{python} {script} runserver {host}:{port}".format(
            python=sys.executable,
            script=manage,
            host="0.0.0.0",
            port=8888,
        )
        return run_command

    def stop(self):
        command = '''ps -ef | grep "{}" | grep -v grep'''.format(self.get_run_command())
        results, code = dandan.system.execute(command)
        results = results.splitlines()
        for result in results:
            match = re.search(r"\w+ +(\d+) +\d+", result)
            if not match:
                continue
            pid = match.group(1)
            command = "kill -9 {}".format(pid)
            logger.info(self.style.ERROR(command))
            os.system(command)

    def start(self):
        self.stop()
        command = self.get_run_command()
        logger.info(self.style.SUCCESS(command))
        os.system(command)

    def back(self):
        self.stop()
        command = "nohup {} 1>/dev/null 2>&1 &".format(self.get_run_command())
        logger.info(self.style.SUCCESS(command))
        os.system(command)

    def restart(self):
        self.stop()
        self.start()
