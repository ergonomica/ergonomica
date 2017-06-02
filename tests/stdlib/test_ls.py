"""
[tests/stdlib/test_ls.py]

Test the ls command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestLs(unittest.TestCase):

    def test_ls(self):
        """
        Test the ls function.
        """
        
        self.assertEqual(ergo('ls'), [os.listdir(".")])
