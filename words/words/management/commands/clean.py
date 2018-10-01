from django.core.management.base import BaseCommand
from django.conf import settings
from django.core import management

import logging
import os
import glob

from words import functions

logger = logging.getLogger("words")


class Command(BaseCommand):
    help = 'Clean project something'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action', '-a',
            type=str,
            required=True,
            help="action type",
            choices=['migrate', 'pyc', 'reset', ])

    def pyc(self):
        for directory, sub_directory, files in os.walk(settings.BASE_DIR):
            for filename in files:
                if not filename.endswith(".pyc"):
                    continue
                pyfile = filename[:-1]
                if pyfile in files:
                    continue
                filename = os.path.join(directory, filename)
                if not os.path.exists(filename):
                    continue
                logger.info(self.style.WARNING("delete {}".format(filename)))
                os.remove(filename)

    def migrate(self):
        os.chdir(settings.BASE_DIR)
        filepattern = "*/migrations/*.py*"
        files = glob.glob(filepattern)
        for filename in files:
            filename = os.path.abspath(filename)
            basename = os.path.basename(filename)
            if basename == "__init__.py":
                continue
            logger.info(self.style.WARNING("delete {}".format(filename)))
            os.remove(filename)

    def reset(self):
        action = functions.input(self.style.ERROR("Realy want to reset? This action will delete all of data!!!"))[0]
        if action not in ("yes", "YES", "y", "Y"):
            return

        self.migrate()
        if os.path.exists(settings.DATABASE_PATH):
            logger.info(self.style.WARNING("delete {}".format(settings.DATABASE_PATH)))
            os.remove(settings.DATABASE_PATH)
        management.call_command("makemigrations")
        management.call_command("migrate")

    def handle(self, *args, **options):
        action = options["action"]
        getattr(self, action)()
