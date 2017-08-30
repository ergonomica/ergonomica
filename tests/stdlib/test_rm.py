#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_rm.py]

Tests the rm command.
"""

import os
import unittest
from ergonomica import ergo

class TestRm(unittest.TestCase):
    """Tests the rm command."""

    def test_rm(self):
        """
        Tests the rm command.
        """

        with open("test_rm_file", "w") as f:
            f.write("example content")

        with open("test_rm_file2", "w") as f:
            f.write("example content")

        # test that files were created properly
        self.assertTrue(os.path.isfile("test_rm_file"))
        self.assertTrue(os.path.isfile("test_rm_file2"))

        ergo("rm test_rm_file test_rm_file2")

        self.assertFalse(os.path.isfile("test_rm_file"))
        self.assertFalse(os.path.isfile("test_rm_file2"))

