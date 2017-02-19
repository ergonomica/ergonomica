# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup_script = ''
if os.name == 'posix':
    setup_script = os.path.join(here, 'ergo_setup.sh')
elif os.name == 'nt':
    setup_script = os.path.join(here, 'ergo_setup.bat')

setup(
    name='ergonomica',
    version='1.1.2',
    description='A cross-platform modern shell written in Python.',
    long_description=long_description,
    url='https://ergonomica.github.io/',
    author='Liam Schumm',
    author_email='liamschumm@icloud.com',
    license='GPL-2.0',

    packages=find_packages(exclude=['tests']),
    install_requires=['ptpython', 'pyflakes', 'pyvim', 'colorama'],
    extras_require={
        'dev': ['pytest'],
    },

    scripts=[setup_script],
    entry_points={
        'console_scripts': [
            'ergonomica=ergonomica.ergo:ergo',
            'ergo=ergonomica.ergo:ergo',
        ],
    },
)

