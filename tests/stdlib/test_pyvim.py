#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_pyvim.py]

Tests the pyvim command.
"""

import unittest

from ergonomica import ergo

class TestPyvim(unittest.TestCase):
    """Tests the pyvim command."""

    # NOTE: as of yet, there isn't really a way of testing this,
    # so just check if it throws an exception (other than PlatformError)

    def test_pyvim(self):
        """
        Tests the pyvim command.
        """

        try:
            ergo("pyvim")
        except Exception as error:
            if error.args[0] == "[ergo]: [pyvim: PlatformError]: Pyvim not supported on this system.":
                pass
            else:
                raise error


