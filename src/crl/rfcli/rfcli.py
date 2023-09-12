import sys
import argparse
import configparser
import os
import re
import socket
import getpass
import textwrap
from distutils import spawn
import yaml
from robot import (
    run_cli,
    pythonpathsetter)
from crl.rfcli._version import get_version
from crl.threadverify import (  # pylint: disable=import-error
    verify_no_new_threads_at_end,
    ThreadVerificationFailed)


__copyright__ = 'Copyright (C) 2019-2024, Nokia'


class RobotCommand(object):

    def __init__(self, options=None, args=None, new_environment_variables=None, debug=False):
        self.options = options
        self.args = args
        self.debug = debug
        self.new_environment_variables = new_environment_variables
        self.full_environment = RobotCommand.build_environment(self.new_environment_variables)
        self.commandline = None

    def __str__(self):
        for variable in self.new_environment_variables:
            print("export " + variable + "=\"" + self.full_environment[variable] + "\"")
        return ' '.join(self.commandline)

    def execute(self):
        if self.debug:
            print("Environment: %s" % self.full_environment)
            print("Commandline: %s" % self.commandline)
        # pylint: disable=unused-variable
        for key, value in self.new_environment_variables.items():
            newpaths = value.split(os.pathsep)
            for path in newpaths:
                pythonpathsetter.add_path(path, True)
        return run_cli(self.commandline[1:], exit=False)  # pylint: disable=unsubscriptable-object

    @staticmethod
    def _check_for_exec(exec_name):
        return True if spawn.find_executable(exec_name) else False

    @staticmethod
    def build_environment(variables):
        new_env = dict(os.environ)
        for key, value in variables.items():
            new_env[key] = value
        return new_env

    @staticmethod
    def is_jybot_installed():
        return RobotCommand._check_for_exec('jybot')

    @staticmethod
    def wrap_help_text(paragraph_list, width):
        wrapped_help_text = [
            textwrap.fill(paragraph, width=width,
                          replace_whitespace=False, drop_whitespace=False)
            for paragraph in paragraph_list]
        return '\n'.join(wrapped_help_text)

    @staticmethod
    def get_argparser():
        mainwidth = 80
        argwidth = 56
        description_text = [
            'A Robot Framework frontend script. All command line options '
            'are passed to pybot/jybot, except for ones listed below.\n',
            'It adds ./libraries and ./resources to PYTHONPATH '
            'so that libraries and resources can easily be '
            'imported in test cases. '
            'Additionally, it will recursively search the ./testcases '
            'directory for any subdirectories named "libraries" or '
            '"resources" and add those to PYTHONPATH.\n',
            'Use rfcli --help to see pybot/jybot help.']
        parser = argparse.ArgumentParser(
            description=RobotCommand.wrap_help_text(description_text, mainwidth),
            add_help=False,
            usage='rfcli [RFCLI OPTIONS] [PYBOT OPTIONS AND ARGUMENTS]',
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument(
            '--version', action='version', version='rfcli %s' % get_version())
        parser.add_argument(
            '--rfcli-output', dest='output',
            help=textwrap.fill(
                'Output directory. (default: $HOME/public_html/rfcli/, '
                'if exists, otherwise ./rfcli_output/', width=argwidth))
        parser.add_argument(
            '--rfcli-help', dest='help', action='store_true', help="Show help for wrapper command")
        parser.add_argument(
            '--rfcli-debug', dest='debug', action='store_true', help="Toggle debug for wrapper command")
        parser.add_argument(
            '--rfcli-show', dest='show', action='store_true',
            help=textwrap.fill(
                "Show pybot/jybot command that would be executed, "
                "but don't execute it.", width=argwidth))
        parser.add_argument(
            '-j', '--jybot', dest='enable_jybot', action='store_true', help="Use jybot "
            "instead of pybot")
        target_help_text = [
            'Target files can use either INI or YAML formats. '
            'Target can be specified in two ways:',
            '(1)  Name of the target system without any extension. '
            'Corresponding "<target>.ini" or "<target>.yaml" file '
            'must exist under "targets" directory.',
            '(2)  <target>.<extension> file with absolute or relative '
            'path and mandatory extension. The <extension> can be ".ini" or ".yaml".\n ',
            'More than one target system can be specified. '
            'Name of the first target will be exported to Robot variable '
            'RFCLI_TARGET_1, second to RFCLI_TARGET_2 and so on.\n',
            'Target properties are read from the INI file and available as '
            'Robot variables {RFCLI_TARGET_1.IP}, {RFCLI_TARGET_1.USER} etc...\n',
            'Target properties in the YAML file can be in a nested structure. '
            'The properties are read from the file. '
            'Each property name is prefixed by the names of each level of '
            'nesting leading to it and separated by ".".\n',
            'The properties are available as Robot variables '
            '{RFCLI_TARGET_1.ENV.PARAMETERS.EXTERNAL_NETWORKS.EXT0}, '
            '{RFCLI_TARGET_1.ENV_PARAMETERS.NTP_SERVERS}, etc...']
        parser.add_argument(
            '-t', '--target', dest='targets', action='append',
            help=RobotCommand.wrap_help_text(target_help_text, argwidth))
        parser.add_argument(
            '--rfcli-no-pythonpath', dest='no_pythonpath', action='store_true',
            help='Do not set PYTHONPATH to libraries.')
        return parser


class PybotCommand(RobotCommand):

    def __init__(self, options=None, args=None, new_environment_variables=None, debug=False):
        super(PybotCommand, self).__init__(options, args, new_environment_variables, debug)
        self.commandline = ['pybot'] + [
            '--listener', 'crl.threadverify.ThreadListener'] + self.options + self.args


class JybotCommand(RobotCommand):

    def __init__(self, options=None, args=None, new_environment_variables=None, debug=False):
        super(JybotCommand, self).__init__(options, args, new_environment_variables, debug)
        self.commandline = ['jybot'] + [
            '--listener', 'crl.threadverify.ThreadListener'] + self.options + self.args


class RobotRunner(object):

    def __init__(self):

        self.calldir = os.getcwd()
        self.parser = RobotCommand.get_argparser()
        self.rfcli_args = None
        self.robot_args = None
        self.help_only = None
        self.parse_args()

    def parse_args(self):
        self.rfcli_args, self.robot_args = self.parser.parse_known_args()
        self.remove_extra_nostatusrc_flags()
        self.help_only = True if self.rfcli_args.help or (len(self.robot_args) < 1) else False

    def remove_extra_nostatusrc_flags(self):
        """
        Bug workaround for --nostatusrc flag functionality: if given twice it will cancel out the effect.

        As this script already adds the --nostatusrc flag, remove all user given such flags when parsing.
        """
        while True:
            try:
                self.robot_args.remove('--nostatusrc')
            except ValueError:
                break

    @property
    def output_directory(self):
        default_html_output_dir = os.path.join(os.path.expanduser('~'), 'public_html', 'rfcli')
        if self.rfcli_args.output:
            return self.rfcli_args.output
        elif os.path.exists(default_html_output_dir):
            return default_html_output_dir
        return 'rfcli_output'

    @property
    def output_under_public_html(self):
        return re.search('/public_html/', self.output_directory)

    def use_jybot(self):
        if self.rfcli_args.enable_jybot:
            if RobotCommand.is_jybot_installed():
                return True
            else:
                raise Exception("Jybot is not installed.")
        return False

    def run(self):
        if self.help_only:
            self.parser.print_help()
            return 0
        if self.use_jybot():
            command = JybotCommand(self.get_robot_options(), self.robot_args, self.get_environment(),
                                   debug=self.rfcli_args.debug)
        else:
            command = PybotCommand(self.get_robot_options(), self.robot_args, self.get_environment(),
                                   debug=self.rfcli_args.debug)
        if self.rfcli_args.show:
            print(command)
            return 0

        try:
            return command.execute()
        finally:
            if self.output_under_public_html:
                print('HTML logs might be located at: http://%s/~%s/rfcli/log.html' % (
                    socket.getfqdn(), self._user_dir_property()))

    @staticmethod
    def _user_dir_property():
        try:
            return getpass.getuser() + '/'
        except TypeError:
            return ''

    def get_robot_options(self):
        robot_options = []
        if self.rfcli_args.targets:
            for i, name in enumerate(self.rfcli_args.targets, start=1):
                filename = os.path.basename(name)
                handler = TargetHandler(name)
                # only target ini file name without path
                robot_options.append('--variable')
                robot_options.append('RFCLI_TARGET_%s:%s' % (
                    i, filename.replace(handler.extension, "")))  # to test
                parsed_options = handler.get_variables()
                for key, value in parsed_options:
                    robot_options.append('--variable')
                    robot_options.append('RFCLI_TARGET_%s.%s:%s' % (i, key, value))
        robot_options.append('-d')
        robot_options.append(self.output_directory)
        robot_options.append('-b')
        robot_options.append('debug.txt')
        robot_options.append('--loglevel')
        robot_options.append('TRACE:INFO')
        robot_options.append('--nostatusrc')
        return robot_options

    def get_environment(self):
        return {} if self.rfcli_args.no_pythonpath else self._get_environment()

    def _get_environment(self):
        testcase_libs = [
            i[0] for i in os.walk(os.path.join(self.calldir, 'testcases'), followlinks=True)
            if re.search(os.path.join('.*', 'libraries$'), i[0])]
        path_list = [self.calldir, os.path.join(
            self.calldir, 'libraries'), os.path.join(
                self.calldir, 'resources')] + testcase_libs
        return {'PYTHONPATH': os.pathsep.join(path_list)}


class IniParser(object):
    def __init__(self, absfilename):
        self.parser = configparser.ConfigParser()
        self.parser.optionxform = str
        self.absfilename = absfilename

    def get_variables(self):
        options = []
        try:
            self.parser.readfp(open(self.absfilename))  # pylint:disable=deprecated-method
        except Exception as e:
            raise Exception("Cannot open target ini file %s: %s" % (self.absfilename, e))
        if not self.parser.has_section('target'):
            raise Exception("Target ini file %s does not have the [target] section" % self.absfilename)
        for key, value in self.parser.items('target'):
            options.append((key, value))
        return options


class YamlParser(object):
    def __init__(self, absfilename):
        self.absfilename = absfilename

    def get_nested_variables(self, variables, key, value):
        if not isinstance(value, dict):
            variables.append((key, value))
        else:
            for k, v in value.items():
                new_key = '%s.%s' % (key, k)
                new_value = v
                variables = self.get_nested_variables(variables, new_key, new_value)
        return variables

    def get_variables(self):
        options = []
        try:
            config = yaml.load(open(self.absfilename))
        except Exception as e:
            raise Exception("Cannot open target yaml file %s: %s" % (self.absfilename, e))
        for key, value in config.items():
            variables = self.get_nested_variables([], key, value)
            for item in variables:
                options.append(item)
        return options


class TargetHandler(object):
    def __init__(self, target_spec):
        self._absfilename = None
        self._extension = None
        self._parser = None
        self.initialize(target_spec)

    @property
    def extension(self):
        if self._extension is not None:
            return self._extension
        else:
            raise Exception("The extension property was not initialized")

    def initialize(self, target_spec):
        if self.target_file_exists(target_spec, '.ini'):
            self.initialize_ini(target_spec)
        elif self.target_file_exists(target_spec, '.yaml'):
            self.initialize_yaml(target_spec)
        else:
            raise Exception("Target file %s does not exist" % target_spec)

    def initialize_ini(self, target_spec):
        self._extension = '.ini'
        self._absfilename = self.expand_absolute_path(
            self.expand_path(target_spec, self._extension))
        self._parser = IniParser(self._absfilename)

    def initialize_yaml(self, target_spec):
        self._extension = '.yaml'
        self._absfilename = self.expand_absolute_path(
            self.expand_path(target_spec, self._extension))
        self._parser = YamlParser(self._absfilename)

    @staticmethod
    def build_path(pathlist):
        return {'PYTHONPATH': ':'.join(pathlist)}

    @staticmethod
    def expand_path(target_spec, extension):
        if not target_spec.endswith(extension):
            if os.path.sep in target_spec:
                expanded_name = target_spec + extension
            else:
                expanded_name = os.path.join('targets', target_spec + extension)
        else:
            expanded_name = target_spec
        return expanded_name

    def target_file_exists(self, filename, extension):
        expanded_name = self.expand_path(filename, extension)
        return os.path.exists(expanded_name)

    @staticmethod
    def expand_absolute_path(target_path):
        if os.path.isabs(target_path):
            absolute_path = target_path
        else:
            absolute_path = os.path.join(os.getcwd(), target_path)
        return absolute_path

    def get_variables(self):
        return self._parser.get_variables()


def get_rfcli_argparser():
    return RobotCommand.get_argparser()


def main():
    try:
        with verify_no_new_threads_at_end():
            status = RobotRunner().run()
        sys.exit(status)
    except ThreadVerificationFailed:
        print('FAILED: at least one test thread is still running.')
        sys.stdout.flush()
        os._exit(1)


if __name__ == "__main__":
    main()
