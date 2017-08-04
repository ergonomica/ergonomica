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

# so the find command won't match this file
UNIQUE_STRING = str(64 - 1)

def makedirstructure():
    """
    Create the directory and file structure for testing the find command.
    """

    global UNIQUE_STRING

    try:
        rmdirstructure()
    except FileNotFoundError:
        pass
        
    os.mkdir("a")
    os.mkdir("b")
    
    with open("a/b.txt", "w") as f, open("b/a.rst", "w") as g, open("a.jpeg", "w") as h:
        f.write("{} {} {}\n".format(UNIQUE_STRING, UNIQUE_STRING, UNIQUE_STRING))
        g.write("321 321 321")
        h.write(UNIQUE_STRING + "\n")
    
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
        self.assertCountEqual(ergo("find file a.*"), ['./a.jpeg',
                                                      './b/a.rst'])
        rmdirstructure()

    def test_flat_find_file(self):
        """
        Tests the find command trying to find files limited to the current directory (non-recursively).
        """

        makedirstructure()
        self.assertCountEqual(ergo("find -f file a.*"), ['a', 'a.jpeg'])
        rmdirstructure()
        
    def test_find_line(self):
        """
        Tests the find command finding a line.
        """

        global UNIQUE_STRING
        
        makedirstructure()
        self.assertCountEqual(ergo("find string {}".format(UNIQUE_STRING)),
                              ["./a/b.txt: {} {} {}".format(UNIQUE_STRING, UNIQUE_STRING, UNIQUE_STRING),
                               "./a.jpeg: {}".format(UNIQUE_STRING)])
        rmdirstructure()

        
    def test_flat_find_line(self):
        """
        Tests the find command trying to find a line limited to the current directory (non-recursively).
        """

        global UNIQUE_STRING
        
        makedirstructure()
        self.assertCountEqual(ergo("find -f string {}".format(UNIQUE_STRING)),
                         ["a.jpeg: {}".format(UNIQUE_STRING)])
        rmdirstructure()
