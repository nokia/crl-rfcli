from __future__ import print_function
from functools import partial
import sys
import threading
import inspect


__copyright__ = 'Copyright (C) 2019, Nokia'


def whatever_io():
    return sys.stdout


class DumpTrace:
    """Dump stacktrace of all saved active threads to *out*.
    The ideas are based on https://gist.github.com/737056."""

    def __init__(self, out=None, sepchr='=', seplen=49):
        self.out = whatever_io() if out is None else out
        self.dprint = partial(print, file=self.out)
        self.sep = sepchr * seplen

    @staticmethod
    def frames():
        return sys._current_frames()

    @property
    def numberofthreads(self):
        return len(self.frames())

    @staticmethod
    def tmap():
        # get a map of threads by their ID so we can print their names
        # during the traceback dump
        return {t.ident: t for t in threading.enumerate()}

    def dump(self):
        self.dprint('Stack dump of all the threads')
        self.dprint(self.sep)
        for tid, frame in self.frames().items():
            self._dump_thread_if_not_junk(tid, frame)

    def _dump_thread_if_not_junk(self, tid, frame):
        thread = self.tmap().get(tid)
        if not thread:
            # skip old junk (left-overs from a fork)
            return
        self._dump_thread(thread, frame)
        self.dprint('')

    def _dump_thread(self, thread, frame):
        self.dprint(f'{thread.name}')
        self.dprint(self.sep)
        self._dump_backtrace(frame)

    def _dump_backtrace(self, frame):
        self.dprint('Traceback (most recent call last):')
        for outer in reversed(inspect.getouterframes(frame)):
            self._dump_frameinfo(outer[0])
            self._dump_frame_locals(outer[0])

    def _dump_frameinfo(self, frame):
        f = inspect.getframeinfo(frame)
        self.dprint(
            '  File: "{f.filename}", line {f.lineno}, in {f.function}\n'
            '    {code}'.format(f=f,
                                code=self._strip(f.code_context[0])))

    @staticmethod
    def _strip(s):
        return s.strip('\n\r\t ')

    def _dump_frame_locals(self, frame, indent=6):
        self.dprint(f"{'':<{indent}}local variables:")
        for n, v in frame.f_locals.items():
            try:
                self.dprint(f"{'':<{indent}}  '{n}': {v!r}")
            except AttributeError as e:
                self.dprint(f"{'':<{indent}}  skipping variable value of '{n}' :{e}")
