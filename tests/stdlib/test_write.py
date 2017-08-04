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
        ergo("print | write test_blank_file")
        
        # check that it's created
        self.assertTrue(os.path.isfile("test_blank_file"))

    def test_write(self):
        """
        Test the write function to write content from STDIN to a file.
        """
        
        # first write to the file
        ergo("print oq4ij 4ojioj1iorj oo4joijoi12' | write {0}")
        
        # then check that the contents are correct
        self.assertEqual(open('test_write_file').read(), "oq4ij\n4ojioj1iorj\noo4joijoi12'")

