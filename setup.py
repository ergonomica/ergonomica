# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import sys
import os

if sys.version_info <= (3, 0):
    print("Sorry, Ergonomica no longer supports Python 2.x.")
    sys.exit()

setup(
    name='ergonomica',
    version='2.0.6',
    description='A cross-platform modern shell written in Python.',
    long_description=open('README.rst').read(),
    url='https://ergonomica.github.io/',
    author='Liam Schumm',
    author_email='liamschumm@icloud.com',
    license='GPL-2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=['six', 'ptpython', 'pyflakes', 'pyvim', 'colorama', 'semver', 'pycron', 'ply', 'psutil', 'docopt', 'requests', 'netifaces'],
    extras_require={
        'dev': ['pytest'],
    },

    entry_points={
        'console_scripts': [
            'ergonomica=ergonomica.ergo:main',
            'ergo=ergonomica.ergo:main',
            ],
        },
)
