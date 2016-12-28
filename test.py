#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[test.py]

Unittests for Ergonomica.
"""

import unittest
from ergonomica import ergo
from lib.lang.ergo2bash import ergo2bash

class TestStringMethods(unittest.TestCase):

    def test_mixed_quotes(self):
        """
        "Single quotes between double quotes not parsing correctly"
        @lschumm
        https://github.com/ergonomica/ergonomica/issues/17
        """
        
        self.assertEqual(ergo("echo \"hello 'world'\""), ["hello 'world'"])

    def test_ergo2bash(self):
        """
        "ergo2bash not working properly for arguments"
        @lschumm
        https://github.com/ergonomica/ergonomica/issues/26
        """

        self.assertEqual(ergo2bash("a b c {d:t} {e:test}").replace("  "," "), "a b c -d -e test")
        
if __name__ == '__main__':
    unittest.main()
