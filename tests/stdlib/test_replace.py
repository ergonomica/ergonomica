#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_replace.py]

Tests the replace command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestReplace(unittest.TestCase):
    """Tests the replace command."""

    def test_add_integers(self):
        """
        Tests adding integers.
        """

        self.assertEqual(ergo('+ 3 5 2 5 3 98124 1984'), [100126])
        
    def test_add_floatingpoint(self):
        """
        Tests adding floating-point numbers.
        """
        
        self.assertEqual(ergo('+ 3.0 5.9 2.4'), [11.3])
        
    def test_add_int_and_floatingpoint(self):
        """
        Tests adding integers and floating-point numbers.
        """
        
        self.assertEqual(ergo('+ 4.9 195401.2 34 2.52 9'), [195451.62])