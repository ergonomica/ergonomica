"""
[tests/stdlib/test_find.py]

Test the find command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestFind(unittest.TestCase):
    """Tests the `find` command."""

    def test_simple_find_stdin(self):
        """
        Test the find function.
        """
        
        self.assertEqual(ergo("print a b c d | find .*"), ['a', 'b', 'c', 'd'])
        
    def test_find_stdin(self):
        """
        """
        
        self.assertItemsEqual(ergo("print abbb acccc ac a oaifjoiafjaosjff fddf | find a[c]+"), ['acccc', 'ac'])

    def test
