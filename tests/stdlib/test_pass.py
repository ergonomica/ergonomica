#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_quit.py]

Tests the quit command.
"""

import unittest

from ergonomica.ergo import ergo

class TestPass(unittest.TestCase):
    """Tests the pass command."""

    def test_pass(self):
        """
        Tests the pass command.
        """

        self.assertEqual(ergo("pass"), None)
