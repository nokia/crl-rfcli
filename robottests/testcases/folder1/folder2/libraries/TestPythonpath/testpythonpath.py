__copyright__ = 'Copyright (C) 2019, Nokia'


class TestPythonpath(object):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.name = 'eeva'
        self.age = 10

    def get_name(self):
        return self.name
