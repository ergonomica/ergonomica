#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_read.py]

Tests the read command.
"""

import os
import unittest
from ergonomica import ergo

class TestRead(unittest.TestCase):
    """Tests the read command."""

    def test_read(self):
        """
        Tests the read command.
        """

        # create the files for testing
        with open("test_read_1", "w") as f, open("test_read_2", "w") as g:
            f.write("a\nb\nc")
            g.write("1\n2\n3")

        # assert that they match what Ergonomica reads
        self.assertEqual(ergo("read test_read_1"), ["a", "b", "c"])
        self.assertEqual(ergo("read test_read_2"), ["1", "2", "3"])

        # delete them
        os.remove("test_read_1")
        os.remove("test_read_2")



