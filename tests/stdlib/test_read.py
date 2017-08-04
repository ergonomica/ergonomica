#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_read.py]

Tests the read command.
"""

import os
import unittest
from ergonomica.ergo import ergo

class TestRead(unittest.TestCase):
    """Tests the read command."""

    def test_read(self):
        """
        Tests the read command.
        """

        # create the files for testing
        with open("test_read_1") as f:
            f.write("a\nb\nc")
        
        with open("test_read_2") as f:
            f.write("1\n\2\n3\n")

        # assert that they match what Ergonomica reads
        self.assertEqual(ergo("read test_read_1"), "a\nb\nc")
        self.assertEqual(ergo("read test_read_2"), "1\n2\n3\n")

        # delete them
        os.remove("test_read_1")
        os.remove("test_read_2")

        
