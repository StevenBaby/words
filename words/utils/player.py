#!/usr/bin/python2
# encoding=utf-8
import sys
import os
import time
import dandan
import random


if dandan.system.is_win32():
    from ctypes import windll, c_buffer

    class _mci:
        def __init__(self):
            self.w32mci = windll.winmm.mciSendStringA
            self.w32mcierror = windll.winmm.mciGetErrorStringA

        def send(self, command):
            buffer = c_buffer(255)
            errorcode = self.w32mci(str(command), buffer, 254, 0)
            if errorcode:
                return errorcode, self.get_error(errorcode)
            else:
                return errorcode, buffer.value

        def get_error(self, error):
            error = int(error)
            buffer = c_buffer(255)
            self.w32mcierror(error, buffer, 254)
            return buffer.value

        def directsend(self, txt):
            (err, buf) = self.send(txt)
            if err != 0:
                print('Error %s for "%s": %s' % (str(err), txt, buf))
            return (err, buf)

    class AudioClip(object):
        def __init__(self, filename):
            filename = filename.replace('/', '\\')
            self.filename = filename
            self._alias = 'mp3_%s' % str(random.random())

            self._mci = _mci()

            self._mci.directsend(r'open "%s" alias %s' % (filename, self._alias))
            self._mci.directsend('set %s time format milliseconds' % self._alias)

            err, buf = self._mci.directsend('status %s length' % self._alias)
            self._length_ms = int(buf)

        def volume(self, level):
            """Sets the volume between 0 and 100."""
            self._mci.directsend('setaudio %s volume to %d' %
                                 (self._alias, level * 10))

        def play(self, start_ms=None, end_ms=None):
            start_ms = 0 if not start_ms else start_ms
            end_ms = self.milliseconds() if not end_ms else end_ms
            err, buf = self._mci.directsend('play %s from %d to %d'
                                            % (self._alias, start_ms, end_ms))

        def isplaying(self):
            return self._mode() == 'playing'

        def _mode(self):
            err, buf = self._mci.directsend('status %s mode' % self._alias)
            return buf

        def pause(self):
            self._mci.directsend('pause %s' % self._alias)

        def unpause(self):
            self._mci.directsend('resume %s' % self._alias)

        def ispaused(self):
            return self._mode() == 'paused'

        def stop(self):
            self._mci.directsend('stop %s' % self._alias)
            self._mci.directsend('seek %s to start' % self._alias)

        def milliseconds(self):
            return self._length_ms

        # TODO: this closes the file even if we're still playing.
        # no good.  detect isplaying(), and don't die till then!
        def __del__(self):
            try:
                self.stop()
                self._mci.directsend('close %s' % self._alias)
            except Exception:
                pass


if len(sys.argv) < 2:
    exit(-1)

filename = str(sys.argv[1])
if not os.path.exists(filename):
    exit(-2)

if not filename.endswith(".mp3"):
    exit(-3)

if dandan.system.is_win32():
    if "back" not in sys.argv:
        os.system('start /b python {0} "{1}" back'.format(__file__, filename))
        exit(0)

    mp3 = AudioClip(filename)
    mp3.play()
    while mp3.isplaying():
        time.sleep(0.01)
    mp3.stop()

elif dandan.system.is_linux():
    os.system('nohup mplayer "{0}" >/dev/null 2>&1 &'.format(filename))
