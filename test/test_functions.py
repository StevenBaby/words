from __future__ import print_function, unicode_literals, absolute_import
import unittest
import os
import sys

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
wordspath = os.path.join(os.path.dirname(dirname), "words")
if wordspath not in sys.path:
    sys.path.insert(0, wordspath)


class TestCase(unittest.TestCase):

    def test_exists(self):
        from words import functions
        self.assertFalse(functions.exists("e"))
        self.assertTrue(functions.exists("apple"))

    def test_consult(self):
        from words import functions
        from words import models
        from dandan import value
        word = functions.consult("apple")
        self.assertTrue(
            isinstance(word, models.Word) or isinstance(word, value.AttrDict)
        )

    def test_console_log(self):
        from words import functions
        import logging
        logger = logging.getLogger('words')
        functions.show_console_log(show=True)
        logger.info("test show log in console")
        functions.show_console_log(show=False)
        logger.info("test hide log in console, but in file")


if __name__ == '__main__':
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
    django.setup()
    unittest.main()
