#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

setup(
    name='ergonomica',
    version='2.5.7',
    description='A cross-platform modern shell written in Python.',
    long_description=open('README.rst').read(),
    url='https://ergonomica.readthedocs.io',
    author='Liam Schumm',
    author_email='contact@hexdump.email',
    license='GPL-2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=['six', 'ptpython', 'pyflakes', 'pyvim', 'colorama', 'pycron', 'psutil', 'docopt', 'requests', 'netifaces', 'semver', 'randomwords', 'watchdog', 'dill'],
    entry_points={
        'console_scripts': [
            'ergonomica=ergonomica.main:run',
            'ergo=ergonomica.main:run',
        ],
    },
)


