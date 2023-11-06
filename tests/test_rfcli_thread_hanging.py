# pylint: disable=unused-argument
import sys
import unittest
import os
import subprocess
from contextlib import contextmanager
import mock
from crl.rfcli.rfcli import main
from .ThreadHanger import ThreadHanger
try:
    from StringIO import StringIO as TestIO
except ImportError:
    from io import StringIO as TestIO


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


class TestThreadHanging(unittest.TestCase):

    @staticmethod
    def _verify_hanging_out(out):
        out = str(out).replace('\\', '')
        assert 'FAILED: at least one test thread is still running.' in out
        assert 'Stack dump of all the threads' in out
        assert "'a': True" in out

    @staticmethod
    @contextmanager
    def threadcleaner():
        t = ThreadHanger()
        try:
            yield t
        finally:
            t.stop()

    @mock.patch('os._exit', side_effect=sys.exit)
    def test_rfcli_with_hanging_threads(self, mock_os_exit):
        self.testdir = os.path.dirname(__file__)
        with self.threadcleaner():
            pro = subprocess.Popen(  # pylint: disable=consider-using-with
                f'rfcli --test "Hang Threads" {self.testdir}',
                shell=True, stdout=subprocess.PIPE)
            self._verify_hanging_out(pro.communicate()[0])
            self.assertEqual(pro.returncode, 1)

    @mock.patch('sys.stdout', new_callable=TestIO)
    @mock.patch('crl.rfcli.rfcli.run_cli')
    @mock.patch('os._exit', side_effect=sys.exit)
    def test_hanging_threads(self, mock_os_exit,
                             mock_run_cli, mock_stdout):
        with self.threadcleaner() as t:
            def run_sideeffect(*args, **kwargs):
                t.start()
            mock_run_cli.side_effect = run_sideeffect
            with self.assertRaises(SystemExit) as se:
                main()
            self.assertEqual(se.exception.code, 1)
            mock_os_exit.assert_called_once_with(1)
            self._verify_hanging_out(mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
