#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_mv.py]

Tests the mv command.
"""

import os
import unittest

from ergonomica.ergo import ergo

class TestMv(unittest.TestCase):
    """Tests the mv command."""

    def test_mv(self):
        """
        Tests the mv command.
        """

        with open("test_mv_file", "w") as f:
            f.write("example content")

        ergo("mv test_mv_file test_mv_file2")

        # ensure the second file has the correct content
        with open("test_mv_file2") as f:
            self.assertEqual(f.read(), "example content")

        # ensure that the last file was deleted
        self.assertFalse(os.path.isfile("test_mv_file"))

        os.remove("test_mv_file2")
