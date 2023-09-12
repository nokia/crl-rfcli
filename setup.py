import os
import imp
from setuptools import setup, find_packages


__copyright__ = 'Copyright (C) 2019, Nokia'

VERSIONFILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'src', 'crl', 'rfcli', '_version.py')


def get_version():
    return imp.load_source('_version', VERSIONFILE).get_version()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='crl.rfcli',
    version=get_version(),
    author='Krisztina Ylinen',
    author_email='krisztina.ylinen@nokia.com',
    description='Robot Framework commands library',
    install_requires=['pyyaml', 'robotframework', 'crl.threadverify'],
    long_description=read('README.rst'),
    license='BSD-3-Clause',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.7',
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
