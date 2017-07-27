#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_equal.py]

Test the equal command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestEqual(unittest.TestCase):
    """Tests the `equal` command."""

    def test_single_element_equal(self):
        """
        Test if equal with one argument will return True.
        """
    
        self.assertItemsEqual(ergo('= 2'), [True])
    
    def test_equal_numbers(self):
        """
        Test the equal function on a series of equal numbers.
        """
        
        self.assertItemsEqual(ergo('= 1 1 1 1 1 1 1 1'), [True])
        
    def test_nequal_numbers(self):
        """
        Test the equal function on a series of not equal numbers.
        """
        
        self.assertItemsEqual(ergo('= 1 1 1 4441 1 1 1 45241 2458925 24'), [False])
        
        
    def test_equal_strings(self):
        """
        Test that two equal strings are returned as equal.
        """
        
        self.assertItemsEqual(ergo('= "testing this\'" "testing this\'"'), [True])
        
        
    def test_nequal_strings(self):
        """
        Test that two not equal strings are returned as equal.
        """
        
        self.assertItemsEqual(ergo('= "testing this\'" "testing thiiis\'"'), [False])
            
    def test_equal_lambda_signatures(self):
        """
        Test that the signature of the same lambda function is equal to itself.
        """
        
        ergo('set a (echo a)')
        self.assertEqual(ergo('= $a $a'), [True])
        ergo('del a')
        