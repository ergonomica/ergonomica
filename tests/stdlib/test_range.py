#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_ls.py]

Tests the range command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestRange(unittest.TestCase):
    """Tests the `range` command."""

    def test_range_end(self):
        """
        Test a range with only an end specified (by default it starts at 0).
        """
        
        self.assertItemsEqual(ergo("range 6"), [0, 1, 2, 3, 4, 5])
        
    def test_range_start_end(self):
        """
        Test a range with start and end specified (by default step is 1).
        """
        
        self.assertItemsEqual(ergo("range 7 9"), [7.0, 8.0])
        
    def test_range_start_end_step(self):
        """
        Test a range with start, end, and step specified.
        """
        
        self.assertItemsEqual(ergo("range 1 10 1"), [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        
    def test_range_start_end_step_undershoot(self):
        """
        Test a range in which (end - start) is not divisible by step.
        """
        
        self.assertItemsEqual(ergo("range 1 10 1.7"), [1.0, 2.7, 4.4, 6.1000000000000005, 7.800000000000001, 9.5])
