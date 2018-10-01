from __future__ import print_function, unicode_literals, absolute_import
import unittest
import os
import glob

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

playpath = os.path.join(os.path.dirname(dirname), "words", "utils", "player.py")


class TestCase(unittest.TestCase):

    def test_player(self):
        if not os.path.exists(playpath):
            raise OSError("file {} not found".format(playpath))
        filepath = os.path.join(dirname, "*.mp3")
        files = glob.glob(filepath)
        for name in files:
            command = '''{} "{}"'''.format(playpath, name)
            print(command)
            os.system(command)
