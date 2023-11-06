# pylint: disable=unused-argument
import sys
import subprocess
import unittest
import os
import mock
from crl.rfcli.rfcli import TargetHandler, main


__copyright__ = 'Copyright (C) 2019, Nokia'


def get_cwd():
    from os import getcwd    # pylint: disable=import-outside-toplevel
    return getcwd()


def osi_path(linux_path):
    """convert a linux path to os-independent path"""
    return linux_path.replace('/', os.path.sep)


class TestRfcliHelpers(unittest.TestCase):
    @mock.patch('os.path.exists')
    def setUp(self, mock_os_path_exists):
        mock_os_path_exists.return_value = True
        self.handler = TargetHandler('my_target_name.ini')
        self.testdir = os.path.dirname(__file__)

    def test_build_path(self):
        path_list1 = ['path1', 'path2']
        result = self.handler.build_path(path_list1)
        self.assertEqual(result, {'PYTHONPATH': 'path1:path2'})
        path_list2 = ['path1', 'path2', 'path3', 'path4', 'path5']
        result = self.handler.build_path(path_list2)
        self.assertEqual(result, {'PYTHONPATH': 'path1:path2:path3:path4:path5'})

    def test_target_expand_with_ini(self):
        result = self.handler.expand_path('my_target_name', '.ini')
        self.assertEqual(result, osi_path('targets/my_target_name.ini'))

    def test_target_expand_with_yaml(self):
        result = self.handler.expand_path('my_target_name', '.yaml')
        self.assertEqual(result, osi_path('targets/my_target_name.yaml'))

    def test_target_expand_ini_with_nothing(self):
        result = self.handler.expand_path('my_target_name.ini', '.ini')
        self.assertEqual(result, 'my_target_name.ini')

    def test_target_expand_yaml_with_nothing(self):
        result = self.handler.expand_path('my_target_name.yaml', '.yaml')
        self.assertEqual(result, 'my_target_name.yaml')

    def test_expand_path_no_extension(self):
        result = self.handler.expand_path('test_file', '.ini')
        self.assertEqual(result, osi_path('targets/test_file.ini'))

        result = self.handler.expand_path(osi_path('somedir/test_file'), '.yaml')
        self.assertEqual(result, osi_path('somedir/test_file.yaml'))

        result = self.handler.expand_path(osi_path('/tmp/test_file'), '.ini')
        self.assertEqual(result, osi_path('/tmp/test_file.ini'))

    @mock.patch('os.path.exists', return_value=True)
    def test_exists_ini_file(self, mock_os_path_exists):
        self.assertTrue(self.handler.target_file_exists('my_target_name.ini', '.ini'))
        expected_calls = [mock.call(self.handler.expand_path('my_target_name.ini', '.ini'))]
        mock_os_path_exists.assert_has_calls(expected_calls)

    @mock.patch('os.path.exists', return_value=True)
    def test_exists_yaml_file(self, mock_os_path_exists):
        self.assertTrue(self.handler.target_file_exists('my_target_name.yaml', '.yaml'))
        expected_calls = [mock.call(self.handler.expand_path('my_target_name.yaml', '.yaml'))]
        mock_os_path_exists.assert_has_calls(expected_calls)

    @mock.patch('os.path.exists', return_value=False)
    def test_not_exists_ini_file(self, mock_os_path_exists):
        self.assertFalse(self.handler.target_file_exists('my_target_name.ini', '.ini'))
        expected_calls = [mock.call(self.handler.expand_path('my_target_name.ini', '.ini'))]
        mock_os_path_exists.assert_has_calls(expected_calls)

    @mock.patch('os.path.exists', return_value=False)
    def test_not_exists_yaml_file(self, mock_os_path_exists):
        self.assertFalse(self.handler.target_file_exists('my_target_name.yaml', '.yaml'))
        expected_calls = [mock.call(self.handler.expand_path('my_target_name.yaml', '.yaml'))]
        mock_os_path_exists.assert_has_calls(expected_calls)

    @mock.patch('os.getcwd', return_value='mocked_cwd')
    def test_expand_absolute_path_relative(self, mock_os_getcwd):
        result = self.handler.expand_absolute_path(osi_path('../../src/alma.ini'))
        self.assertEqual(result, osi_path('mocked_cwd/../../src/alma.ini'))

        result = self.handler.expand_absolute_path('alma.ini')
        self.assertEqual(result, osi_path('mocked_cwd/alma.ini'))

    def test_expand_absolute_path_absolute(self):
        self.assertEqual(
            self.handler.expand_absolute_path(
                osi_path('/home/fedora/gitlab/crl-rfcli/src/alma.ini')),
            osi_path('/home/fedora/gitlab/crl-rfcli/src/alma.ini'))

    def test_rfcli_dummy(self):
        with subprocess.Popen(f"rfcli --test Dummy {self.testdir}",
                              shell=True, stdout=subprocess.PIPE) as pro:
            self.assertIn(b'Dummy', pro.communicate()[0])
            self.assertEqual(pro.returncode, 0)

    @mock.patch('crl.rfcli.rfcli.run_cli',
                side_effect=lambda *args, **kwargs: [sys.exit(0), exit])
    def test_main(self, mock_run_cli):
        with mock.patch.object(sys, 'argv', ['rfcli', 'test']):
            with self.assertRaises(SystemExit) as se:
                main()
            self.assertEqual(se.exception.code, 0)
        mock_run_cli.assert_called_once_with([
            '--listener', 'crl.threadverify.ThreadListener',
            '-d', 'rfcli_output', '-b', 'debug.txt',
            '--loglevel', 'TRACE:INFO', '--nostatusrc', 'test'], exit=False)


if __name__ == '__main__':
    unittest.main()
