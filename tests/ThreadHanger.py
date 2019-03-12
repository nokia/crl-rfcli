import threading


__copyright__ = 'Copyright (C) 2019, Nokia'


class _ThreadHanger(threading.Thread):
    def __init__(self):
        super(_ThreadHanger, self).__init__(target=self.run, name='HangingThread')
        self.keeprunning = None
        self.started = False

    def __enter__(self):
        self.start()

    def __exit__(self, *args, **kwargs):
        self.stop()

    def run(self):
        a = self.keeprunning
        self.started = True
        while a:
            a = self.keeprunning

    def start(self):
        self.keeprunning = True
        super(_ThreadHanger, self).start()

    @staticmethod
    def stop():
        for t in threading.enumerate():
            if t.name == 'HangingThread':
                t.keeprunning = False
                t.join()


class ThreadHanger(object):
    def __init__(self):
        self._threadhanger = _ThreadHanger()

    def __enter__(self):
        self._threadhanger.start()

    def __exit__(self, *args, **kwargs):
        self._threadhanger.stop()

    def run(self):
        self._threadhanger.run()

    def start(self):
        self._threadhanger.start()

    def stop(self):
        self._threadhanger.stop()
