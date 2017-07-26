#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_print.py]

Test the print command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestPrint(unittest.TestCase):
    """Tests the `print` command."""

    def test_single_print(self):
        """
        Test printing a single string.
        """
        
        self.assertEqual(ergo('print "this is an example of a \'string\'"'), ["this is an example of a 'string'"])
        
    
    def test_multi_print(self):
        """
        Test printing multiple strings.
        """
        
        self.assertEqual(ergo('print these are a collection of strings'), ['these', 'are', 'a', 'collection', 'of', 'strings'])
    
    
    def test_multiplication(self):
        """
        Test multiplying a string for printing.
        """
        
        self.assertEqual(ergo('print a b a b -m 2'), ['a', 'b', 'a', 'b', 'a', 'b', 'a', 'b'])
