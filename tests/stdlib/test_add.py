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

    def test_add(self):
        """
        Test adding numbers.
        """
        
        self.assertEqual(ergo('+ 3 5 2 5 3 98124 1984'), [100126])

    # TODO: finish this
    # def test_add_stringerror(self):
    #     """
    #     Test that add throws the correct error when strings are passed.
    #     """
    #
    #     self.assertEqual(ergo('+ 4 14tj1oitfdfafafa`ffff`'))
