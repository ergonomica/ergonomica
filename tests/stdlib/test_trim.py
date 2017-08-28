#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_trim.py]

Tests the trim command.
"""

import unittest
from ergonomica import ergo

class TestTrim(unittest.TestCase):
    """Tests the trim command."""

    def test_trim(self):
        """
        Tests the trim command.
        """

        self.assertEqual(ergo("trim \" abc \""), "abc")
        self.assertEqual(ergo("trim head \" abc \""), "abc ")
        self.assertEqual(ergo("trim tail \" abc \""), " abc")
        