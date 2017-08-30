#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_exit.py]

Tests the exit command.
"""

import unittest

from ergonomica import ergo

class TestExit(unittest.TestCase):
    """Tests the exit command."""

    # NOTE: as of yet, there isn't really a way of testing this,
    # so just check if it throws an exception

    def test_exit(self):
        """
        Tests the exit command.
        """

        ergo("exit")

