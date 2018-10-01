from __future__ import print_function
import sys
import os
import glob
import unittest

filepath = os.path.abspath(__file__)
dirname = os.path.dirname(filepath)
wordspath = os.path.join(os.path.dirname(dirname), "words")
if wordspath not in sys.path:
    sys.path.insert(0, wordspath)


def test_all():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(test_dir, "test_*.py")

    module_names = map(lambda f: os.path.splitext(os.path.basename(f))[0], glob.glob(filename))
    modules = map(__import__, module_names)

    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))


def test_player():
    load = unittest.defaultTestLoader.loadTestsFromModule
    module = __import__("test_player")
    return unittest.TestSuite(load(module))


def test_no_voice():
    voices = [
        "test_player",
    ]

    test_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(test_dir, "test_*.py")
    module_names = map(lambda f: os.path.splitext(os.path.basename(f))[0], glob.glob(filename))

    nvoices = [var for var in module_names if var not in voices]

    modules = map(__import__, nvoices)

    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))


if __name__ == '__main__':
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
    django.setup()
    unittest.main(defaultTest="test_no_voice")
