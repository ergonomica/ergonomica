# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

#here = os.path.abspath(os.path.dirname(__file__))
#return open(os.path.join(os.path.dirname(__file__), fname)).read()

#setup_script = ''
#removal_script = ''

setup(
    name='ergonomica',
    version='2.0.0-b26',
    description='A cross-platform modern shell written in Python.',
    long_description=open('README.rst').read(),
    url='https://ergonomica.github.io/',
    author='Liam Schumm',
    author_email='liamschumm@icloud.com',
    license='GPL-2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=['six', 'ptpython', 'pyflakes', 'pyvim', 'colorama', 'semver', 'pycron', 'ply', 'psutil', 'docopt'],
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
