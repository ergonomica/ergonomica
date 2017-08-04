#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_write.py]

Test the write command.
"""

import os
import unittest

from ergonomica.ergo import ergo

class TestWrite(unittest.TestCase):
    """Tests the write command."""

    def test_write(self):
        """
        Tests the write command.
        """
        
        # first write to the file
        ergo("print oq4ij 4ojioj1iorj oo4joijoi12 | write test_write_file {0}")
        
        # then check that the contents are correct
        with open("test_write_file") as f:
            self.assertEqual(f.read(), "oq4ij\n4ojioj1iorj\noo4joijoi12'\n")

        # then cleanup
        os.remove("test_write_file")
