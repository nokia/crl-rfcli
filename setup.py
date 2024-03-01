import os
import importlib
from setuptools import setup, find_packages


__copyright__ = 'Copyright (C) 2019-2024, Nokia'

VERSIONFILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'src', 'crl', 'rfcli', '_version.py')


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_version():
    return import_module("_version", VERSIONFILE).get_version()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='crl.rfcli',
    version=get_version(),
    author='Krisztina Ylinen',
    author_email='krisztina.ylinen@nokia.com',
    description='Robot Framework commands library',
    install_requires=['pyyaml',
                      'robotframework>=3.1',
                      'crl.threadverify'],
    long_description=read('README.rst'),
    license='BSD-3-Clause',
    python_requires='>=3.7,<3.13',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11',
                 'Programming Language :: Python :: 3.12',
                 'Framework :: Robot Framework :: Tool',
                 'Topic :: Software Development'],
    keywords='robotframework',
    url='https://github.com/nokia/crl-rfcli',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['crl'],
    entry_points={
        'console_scripts': [
            'rfcli = crl.rfcli.rfcli:main'
        ]
    }
)
