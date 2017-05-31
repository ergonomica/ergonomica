# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup_script = ''
removal_script = ''
if os.name == 'posix':
    setup_script = os.path.join(here, 'scripts/ergo_setup.sh')
    removal_script = os.path.join(here, 'scripts/ergo_remove.sh')
elif os.name == 'nt':
    setup_script = os.path.join(here, 'scripts/ergo_setup.bat')

setup(
    name='ergonomica',
    version='2.0.0-b13',
    description='A cross-platform modern shell written in Python.',
    long_description=read('README.rst'),
    url='https://ergonomica.github.io/',
    author='Liam Schumm',
    author_email='liamschumm@icloud.com',
    license='GPL-2.0',

    packages=find_packages(exclude=['tests']),
    install_requires=['ptpython', 'pyflakes', 'pyvim', 'colorama', 'semver', 'pycron', 'ply', 'psutil'],
    extras_require={
        'dev': ['pytest'],
    },

    scripts=[setup_script],
    entry_points={
        'console_scripts': [
            'ergonomica=ergonomica.ergo:main',
            'ergo=ergonomica.ergo:main',
            ],
        },
)
