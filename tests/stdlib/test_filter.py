#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_filter.py]

Test the filter command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestFilter(unittest.TestCase):
    """Tests the `filter` command."""

    def test_filter(self):
        """
        Test filtering STDIN.
        """
        
        self.assertEqual(ergo('print 1 3 2 4 | filter 0 2'), ['1', '2'])
