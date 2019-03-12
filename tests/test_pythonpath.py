import os
import shutil
from xml.etree import ElementTree
import pytest
from temp_utils.contextmanagers import chdir


__copyright__ = 'Copyright (C) 2019, Nokia'

THISDIR = os.path.dirname(__file__)
ROBOTEXAMPLE = os.path.join(THISDIR, 'robotexample')


@pytest.fixture
def robotdir(tmpdir):
    with tmpdir.as_cwd():
        shutil.copytree(ROBOTEXAMPLE, 'robotexample')
        with chdir('robotexample'):
            yield None


@pytest.fixture
def clean_pythonpath_run(script_runner):
    env = os.environ.copy()
    if 'PYTHONPATH' in env:
        del env['PYTHONPATH']

    def run(cmd, *args):
        return script_runner.run_subprocess(cmd, *args, env=env)

    return run


@pytest.mark.usefixtures('robotdir')
def test_pythonpath(clean_pythonpath_run):
    ret = clean_pythonpath_run('rfcli', '-t', 'example', 'testcases')
    assert ret.success, (ret.stdout, ret.stderr)
    assert not _errors()


@pytest.mark.usefixtures('robotdir')
def test_no_pythonpath(clean_pythonpath_run):
    ret = clean_pythonpath_run('rfcli', '--rfcli-no-pythonpath', '-t', 'example', 'testcases')
    assert ret.success, (ret.stdout, ret.stderr)
    assert "Importing test library 'example' failed" in _errors()


def test_no_pythonpath_help(script_runner):
    ret = script_runner.run('rfcli', '--rfcli-help')
    assert 'Do not set PYTHONPATH to libraries.' in ret.stdout


def _errors():
    root = ElementTree.parse('rfcli_output/output.xml')
    return '\n'.join([e.text for e in root.find('errors')])
