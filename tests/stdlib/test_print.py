#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_print.py]

Test the print command.
"""

import unittest
import os

from ergonomica import ergo


class TestPrint(unittest.TestCase):
    """Tests the `print` command."""

    def test_single_print(self):
        """
        Test printing a single string.
        """

        self.assertEqual(ergo('print "this is an example of a \'string\'"'), "this is an example of a 'string'")

