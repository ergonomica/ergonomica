#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_pyvim.py]

Defines the "pyvim" command.
"""

from __future__ import unicode_literals

try:
    from pyvim.entry_points.run_pyvim import run

    def main(argc):
        """
        pyvim: Pure Python Vim clone.

        Usage:
            pyvim [FILES...]
        """

        # seemingly extraneous
        # pylint: disable=too-many-function-args
        run(argc.args['FILES'])

except ImportError:
    print("[ergo] [pyvim: PlatformError]: Pyvim not supported on this system;\
          probably Travis CI. `pyvim` command will now raise an exception on\
          invocation.")

    def main(argc):
        """
        pyvim: Pure Python Vim clone.

        Usage:
            pyvim [FILES,...]
        """

        raise Exception("[ergo] [pyvim: PlatformError]: Pyvim not supported on \
                        this system.")
