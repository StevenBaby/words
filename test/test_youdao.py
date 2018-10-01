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

    def test_get_word(self):
        from utils import youdao
        from dandan import value

        word = youdao.get_word("apple")
        print(word)
        self.assertIsInstance(word, value.AttrDict)
        self.assertEqual(word.title, "apple")

    def test_get_phonetic(self):
        from utils import youdao

        titles = [
            "apple",
            "love me love my dog",
        ]

        for title in titles:
            filename = os.path.abspath("{}.mp3".format(title))
            if os.path.exists(filename):
                os.remove(filename)
            self.assertFalse(os.path.exists(filename))
            youdao.get_phonetic(title, filename)
            self.assertTrue(os.path.exists(filename))


if __name__ == '__main__':
    unittest.main()
