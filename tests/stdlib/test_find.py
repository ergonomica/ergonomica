#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_find.py]

Test the find command.
"""

import os
import shutil
import unittest

from ergonomica.ergo import ergo

def makedirstructure():
    """
    Create the directory and file structure for testing the find command.
    """
    
    os.mkdir("a")
    os.mkdir("b")
    open("a/b.txt", "w").write("123 123 123")
    open("b/a.rst", "w").write("321 321 321")
    open("a.jpeg", "w").write("123")
    
def rmdirstructure():
    """
    Delete the directory and file structure created for testing the find command.
    """

    shutil.rmtree("a")
    shutil.rmtree("b")
    os.remove("a.jpeg")

class TestFind(unittest.TestCase):
    """Tests the find command."""

    def test_find_file(self):
        """
        Tests the find command trying to find files.
        """
        
        makedirstructure()
        self.assertEqual(ergo("find file a.*"), ['./b/a.rst'])
        rmdirstructure()

    def test_flat_find_file(self):
        """
        Tests the find command trying to find files limited to the current directory (non-recursively).
        """

        makedirstructure()
        self.assertEqual(ergo("find -f file a.*"), [])
        rmdirstructure()
        
    def test_find_line(self):
        """
        Tests the find command finding a line.
        """

        makedirstructure()
        self.assertEqual(ergo("find string 123"),
                         ["./a/b.txt: 123 123 123",
                          "./a.jpeg: 123"])
        rmdirstructure()

        
    def test_flat_find_line(self):
        """
        Tests the find command trying to find a line limited to the current directory (non-recursively).
        """
        makedirstructure()
        self.assertEqual(ergo("find string 123"),
                         ["./a.jpeg: 123"])
        rmdirstructure()
        
