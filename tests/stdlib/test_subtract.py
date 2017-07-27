#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_subtract.py]

Test the subtract command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestSubtract(unittest.TestCase):
    """Tests the 'subtract' command."""

    def test_subtract_int(self):
        """
        Test subtracting two integers.
        """
        
        self.assertEqual(ergo('- 2 4'), [-2.0])

    def test_subtract_int(self):
        """
        Test subtracting two floating point numbers.
        """
        
        self.assertEqual(ergo('- 2 5.0'), [-3.0])
