# pylint: disable=unused-argument
import pytest
from crl.rfcli.rfcli import RobotRunner


__copyright__ = 'Copyright (C) 2019, Nokia'


@pytest.fixture()
def monkeypatch_attributes(monkeypatch):
    monkeypatch.setattr("socket.getfqdn", lambda: "test.fqdn.com")
    monkeypatch.setattr("crl.rfcli.rfcli.RobotRunner.output_under_public_html",
                        lambda: True)


@pytest.mark.parametrize("uservar", [
    {"USER": "testuser", "USERNAME": None, "LNAME": None, "LOGNAME": None},
    {"USER": None, "USERNAME": "testuser", "LNAME": None, "LOGNAME": None},
    {"USER": None, "USERNAME": None, "LNAME": "testuser", "LOGNAME": None},
    {"USER": None, "USERNAME": None, "LNAME": None, "LOGNAME": "testuser"}, ])
def test_user_dir_property_with_user(uservar, capsys, monkeypatch_attributes, monkeypatch):
    monkeypatch.setattr("os.environ", uservar)
    s = RobotRunner()
    try:
        s.run()
    except SystemExit:
        pass
    finally:
        stdout, _ = capsys.readouterr()
        assert stdout == "HTML logs might be located at: " \
                         "http://test.fqdn.com/~testuser//rfcli/log.html\n"


def test_user_dir_property_no_user(capsys, monkeypatch_attributes, monkeypatch):
    monkeypatch.setattr("getpass.getuser", {})
    s = RobotRunner()
    try:
        s.run()
    except SystemExit:
        pass
    finally:
        stdout, _ = capsys.readouterr()
        assert stdout == "HTML logs might be located at: " \
                         "http://test.fqdn.com/~/rfcli/log.html\n"
