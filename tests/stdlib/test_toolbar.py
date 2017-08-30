#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_toolbar.py]

Tests the toolbar command.
"""

import unittest

from ergonomica import ergo

class TestToolbar(unittest.TestCase):
    """Tests the toolbar command."""

    # NOTE: as of yet, there isn't really a way of testing this,
    # so just check if it throws an exception

    def test_toolbar(self):
        """
        Tests the toolbar command.
        """

        ergo("toolbar 123")

