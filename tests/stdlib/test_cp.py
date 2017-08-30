#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_cp.py]

Tests the cp command.
"""

import os
import unittest
from ergonomica import ergo

class TestCp(unittest.TestCase):
    """Tests the cp command."""

    def test_cp(self):
        """
        Tests the cp command.
        """

        with open("test_cp_file", "w") as f:
            f.write("example content")

        ergo("cp test_cp_file test_cp_file2")

        # ensure the second file has the correct content
        self.assertEqual(open("test_cp_file2").read(), "example content")

        # ensure that the last file was not deleted
        self.assertEqual(open("test_cp_file").read(), "example content")

        os.remove("test_cp_file")
        os.remove("test_cp_file2")

