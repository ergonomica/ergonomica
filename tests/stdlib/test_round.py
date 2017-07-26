#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_round.py]

Tests the round command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestRound(unittest.TestCase):
    """Tests the 'round' command."""


    def test_round_integer_to_integer(self):
        """
        Test rounding a series of integers back to integers.
        """
        
        self.assertItemsEqual(ergo('print 1 2 3 4 | round'), [1, 2, 3, 4)

    
    def test_round_integer_to_float(self):
        """
        Test rounding a series of integers to a float.
        """
        
        self.assertItemsEqual(ergo('print 1337 1377 1773 | round 1'), [1337.0, 1377.0, 1773])
    

    def test_round_float_to_integer(self):
        """
        Test rounding a float to an integer.
        """
        
        self.assertItemsEqual(ergo('print 1.0 | round'), [1])    
        
    def test_round_float_to_float(self):
        """
        Test rounding a series of floats to floats.
        """
        
        self.assertItemsEqual(ergo('print 1.0342 4.91051 3.1415926 | round 3'), [1.034, 4.911, 3.142])
