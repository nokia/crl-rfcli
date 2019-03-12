.. Copyright (C) 2019, Nokia

.. image:: https://travis-ci.org/nokia/crl-rfcli.svg?branch=master
    :target: https://travis-ci.org/nokia/crl-rfcli

Robot Framework Frontend Library
================================

About
-----

Robot Framework frontend script.

Documentation
-------------

Documentation for ``crl.rfcli`` can be found from `Read The Docs`_.

.. _Read The Docs: http://crl-rfcli.readthedocs.io/

Installation
------------

The package can be installed with pip::

  # pip install crl.rfcli

Test Execution
--------------

Test cases are executed with "rfcli" command. It adds **./libraries** and
**./resources** to PYTHONPATH so that you can easily import libraries and resources
in test cases.
Additionally, it will recursively search the **./testcases** directory for
any subdirectories named **libraries** or **resources** and add those to PYTHONPATH.

**Rfcli** reads the target information for targets specified with **-t option** from
config files. The target config files can be either in INI or YAML format.
It exports the variables to the test execution environment as RFCLI_TARGET_1.IP etc.
Use the -t and --rfcli-show options together to see how it works.

Test case output is directed to *$HOME/public_html/rfcli* if the directory
exists.

Examples
--------

::

    rfcli -t foundcloud1 --suite framework.use_targets testcases

The target parameter can be specified in the following ways:

#. The name of the target system can be specified without any extension.
   The corresponding file with the .ini or .yaml extension must exist in the targets directory.::

    rfcli -t targetname

#. A target file can be specified with an absolute or a relative path including one of the supported extensions.
   The extension can be .ini or .yaml::

    rfcli -t /home/fedora/gitlab/crl/targetname.ini
    rfcli -t ../../gitlab/crl/targetname.ini

    rfcli -t /home/fedora/gitlab/crl/targetname.yaml
    rfcli -t ../../gitlab/crl/targetname.yaml

More than one target system can be specified.

The name of each target will be exported to an enumerated Robot variable.  The
name of the first target will be exported to RFCLI_TARGET_1, the second one to
RFCLI_TARGET_2 and so on.

The target properties are read from the INI file and later available as Robot
variables RFCLI_TARGET_1.IP, RFCLI_TARGET_2.USER, etc...

The target properties in the YAML file can be in a nested structure.  The
properties are read from the file.  Each property name is prefixed by the names
of each level of nesting leading to it and separated by ".".  The properties
are available as Robot variables
RFCLI_TARGET_1.ENV.PARAMETERS.EXTERNAL_NETWORKS.EXT0,
RFCLI_TARGET_1.ENV_PARAMETERS.NTP_SERVERS, etc...

Contributing
------------

Please see contributing_ for development and contribution practices.

The code_ and the issues_ are hosted on GitHub.

The project is licensed under BSD-3-Clause_.

.. _contributing: https://github.com/nokia/crl-rfcli/blob/master/CONTRIBUTING.rst
.. _code: https://github.com/nokia/crl-rfcli
.. _issues: https://github.com/nokia/crl-rfcli/issues
.. _BSD-3-Clause:  https://github.com/nokia/crl-rfcli/blob/master/LICENSE
