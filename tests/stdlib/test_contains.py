#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_contains.py]

Test the contains command.
"""

import unittest

from ergonomica.ergo import ergo

class TestContains(unittest.TestCase):
    """Tests the contains command."""

    def test_contains_singlevar_true(self):
        """
        Tests the contains function with one variable on something that should return true.
        """
        
        self.assertEqual(ergo("print 1 2 3 | contains 1"), [True])

    def test_contains_multivar_true(self):
        """
        Tests the contains function with multiple variables on something that should return true.
        """
        
        self.assertEqual(ergo("print 1 2 6 4 a | contains a 6"), [True])

    def test_contains_singlevar_false(self):
        """
        Tests the contains function with one variable on something that should return false.
        """
        
        self.assertEqual(ergo("print 1 2 3 | contains aaoigrjoasgjo"), [False])

    def test_contains_multivar_true(self):
        """
        Tests the contains function with multiple variables on something that should return false.
        """
        
        self.assertEqual(ergo("print 1 2 6 4 a | contains 9 1"), [False])
    


