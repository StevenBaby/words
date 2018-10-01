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

    def test_styles(self):
        from words import styles
        modules = dir(styles)
        for name in modules:
            attr = getattr(styles, name)
            if not callable(attr):
                continue
            print(attr(name))


if __name__ == '__main__':
    unittest.main()
