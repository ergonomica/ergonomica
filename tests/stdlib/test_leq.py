#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_leq.py]

Tests the leq command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestLeq(unittest.TestCase):
    """Tests the leq command."""
    
    
    def test_integer_integer(self):
        """
        Test leq on two integers.
        """
        
        self.assertEqual(ergo("<= 3 4"), [True])
        
        
    def test_integer_float(self):
        """
        Tests leq on an integer and a float.
        """
        
        self.assertEqual(ergo("<= 3 3.04"), [True])
        
        
    def test_float_integer(self):
        """
        Tests leq on a float and an integer.
        """
        
        self.assertEqual(ergo("<= 9.02 1"), [False])
        
        
    def test_float_float(self):
        """
        Tests leq on two floats.
        """
        
        self.assertEqual(ergo("<= 1.003 1.000"), [False])

