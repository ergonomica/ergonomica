# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

setup(
    name='ergonomica',
    version='2.0.7',
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
