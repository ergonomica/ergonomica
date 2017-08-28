#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_title.py]

Tests the title command.
"""

import unittest

from ergonomica import ergo

class TestTitle(unittest.TestCase):
    """Tests the title command."""
    
    # NOTE: as of yet, there isn't really a way of testing this,
    # so just check if it throws an exception

    def test_title(self):
        """
        Tests the title command.
        """

        ergo("title 123")
