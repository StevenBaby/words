from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Show default style of django'

    def handle(self, *args, **options):
        styles = [var for var in dir(self.style) if not var.startswith("__")]
        for style in styles:
            func = getattr(self.style, style)
            if not callable(func):
                continue
            print(func(style))
