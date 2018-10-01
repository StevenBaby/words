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

    def test_qsbdc(self):
        import resources
        self.assertIsInstance(resources.get_resources(), list)


if __name__ == '__main__':
    unittest.main()
