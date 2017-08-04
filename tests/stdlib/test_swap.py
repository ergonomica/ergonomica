#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_swap.py]

Tests the swap command.
"""

import os
import unittest
from ergonomica.ergo import ergo

class TestSwap(unittest.TestCase):
    """Tests the swap command."""

    def test_swap(self):
        """
        Tests the swap command.
        """

        with open("test_swap_file", "w") as f:
            f.write("example content 1")

        with open("test_swap_file2", "w") as f:
            f.write("example content 2")

        # assert that contents are in the right files
        self.assertEqual(open("test_swap_file").read(), "example content 1")
        self.assertEqual(open("test_swap_file2").read(), "example content 2")

        # swap them
        ergo("swap test_swap_file test_swap_file2")

        # assert that contents are switched
        self.assertEqual(open("test_swap_file").read(), "example content 2")
        self.assertEqual(open("test_swap_file2").read(), "example content 1")

        # cleanup
        os.remove("test_swap_file")
        os.remove("test_swap_file2")
