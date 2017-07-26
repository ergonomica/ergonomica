#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_write.py]

Test the write command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestWrite(unittest.TestCase):
    """Tests the `addstring` command."""

    def test_write_blank_file(self):
        """
        Test writing a blank file.
        """
        
        # create the file
        
        self.assertEqual(ergo("")

    def test_write(self):
        """
        Test the write function to write content from STDIN to a file.
        """
        
        self.assertEqual(ergo("print oq4ij 4ojioj1iorj oo4joijoi12' | addstring"), ["oq4ij4ojioj1iorjoo4joijoi12'"])
