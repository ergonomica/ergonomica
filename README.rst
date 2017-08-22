Ergonomica
==========

|pypi| |issues|

`Wiki`_ | `GitHub Repo`_ | `Download Binaries`_ | `Issue Tracker`_

Ergonomica is a cross-platform shell language, implemented in Python. Ergonomica aims to modernize the terminal, in an easily-extensible and usable language, independent of the OS on which it runs. It uses existing core utilities such as the `os` and `shutil` packages, as well as other utilities written in Python, such as the `pyvim` editor, providing built-in tools that are not os-dependent. Existing Python language features such as asynchronous returning may replace components of the shell such as piping.

- Stable Branch: master
- Development branch: develop
- Feature branches: feature/*
- Release branches: release/*
- CodeClimate: |codeclimate|
- Travis CI: |travisci|
- License: |license|

How to Install?
===============

See `installation page`_.

Credits
=======
`@lschumm`_, Lead Developer. `@appleinventor`_, `@schtolc`_, `@dpp2000`_, Developers.

Ergonomica couldn't work without:

- `@jonathanslenders`_\'s amazing `prompt_toolkit`_ and `pyvim`_ (implemented in `prompt_toolkit`_)
- `@tartley`_\'s `Colorama`_

Security
========

If you find an exploit in Ergonomica, please contact either `@lschumm`_ or `@insertplus`_ through `Keybase`_.

.. _Wiki: https://ergonomica.readthedocs.io

.. _GitHub Repo: https://github.com/ergonomica/ergonomica

.. _Download Binaries: https://github.com/ergonomica/ergonomica/releases

.. _Issue Tracker: https://github.com/ergonomica/ergonomica/issues

.. _installation page: https://github.com/ergonomica/ergonomica/wiki/Installation

.. _Colorama: https://github.com/tartley/colorama

.. _Suplemon: https://github.com/richrd/suplemon

.. _@lschumm: https://github.com/lschumm

.. _@appleinventor: https://github.com/appleinventor

.. _@schtolc: https://github.com/schtolc

.. _@dpp2000: https://github.com/dpp2000

.. _@jonathanslenders: https://github.com/jonathanslenders

.. _prompt_toolkit: https://github.com/jonathanslenders/prompt_toolkit

.. _pyvim: https://github.com/jonathanslenders/pyvim

.. _@tartley: https://github.com/tartley/colorama

.. _@lschumm: https://keybase.io/lschumm

.. _@insertplus: https://keybase.io/insertplus

.. _Keybase: https://keybase.io


.. |pypi| image:: https://img.shields.io/badge/pypi-2.2.0-blue.svg
   :target: https://pypi.python.org/pypi/ergonomica/2.2.0
   :alt: Pip Version 2.2.0

.. |license| image:: https://img.shields.io/github/license/ergonomica/ergonomica.svg


.. |issues| image:: https://img.shields.io/github/issues/ergonomica/ergonomica.svg
   :target: https://github.com/ergonomica/ergonomica/issues
   :alt: Ergonomica logo.

.. |codeclimate| image:: https://codeclimate.com/github/ergonomica/ergonomica/badges/gpa.svg?style=flat-square
    :target: https://codeclimate.com/github/ergonomica/ergonomica
    :alt: Code Climate

.. |travisci| image:: https://travis-ci.org/ergonomica/ergonomica.svg?branch=master
   :target: https://travis-ci.org/ergonomica/ergonomica
   :alt: Travis CI Build Status
