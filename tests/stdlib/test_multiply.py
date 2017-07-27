#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_multiply.py]

Tests the multiply command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestMultiply(unittest.TestCase):
    """Tests the `ls` command."""

    def test_multiply_integers(self):
        """
        Tests multiplying integers.
        """

        self.assertEqual(ergo('* 4 6 4 13413'), [1287648])

    def test_multiply_floatingpoint(self):
        """
        Tests multiplying floating-point numbers.
        """
        
        self.assertEqual(ergo('* 3.0 6.0 1.0'), [18.0])
        
    def test_multiply_int_and_floatingpoint(self):
        """
        Tests multiplying integers and floating-point numbers.
        """
        
        self.assertEqual(ergo('* 5104 4.2 901 1.1'), [21246012.480000004])
