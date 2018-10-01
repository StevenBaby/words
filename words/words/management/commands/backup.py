from django.core.management.base import BaseCommand
import os
import glob

from django.conf import settings

from words import functions


class Command(BaseCommand):
    help = 'Backup current database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action', '-a',
            type=str,
            required=True,
            help="action type",
            choices=['backup', 'restore', 'show', ])

    def show(self):
        filename = os.path.join(settings.BACKUP_PATH, "*words.db")
        files = sorted(glob.glob(filename), reverse=True)
        for filename in files:
            print(os.path.basename(filename))

    def restore(self):
        functions.restore()

    def backup(self):
        functions.backup()

    def handle(self, *args, **options):
        action = options["action"]
        func = getattr(self, action)
        func()
