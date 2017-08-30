#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_quit.py]

Tests the quit command.
"""

import unittest

from ergonomica import ergo

class TestQuit(unittest.TestCase):
    """Tests the quit command."""

    # NOTE: as of yet, there isn't really a way of testing this,
    # so just check if it throws an exception

    def test_quit(self):
        """
        Tests the quit command.
        """

        ergo("quit")

