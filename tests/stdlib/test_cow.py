#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_cow.py]

Tests the cow command.
"""

import unittest
from ergonomica import ergo

def makevalidcow(string):
    return " " + "_" * (len(string) + 2) + "\n" \
          + "< %s >\n" % string \
          + " " + "-" * (len(string) + 2) \
          + """
    \\    ^__^
     \\   (oo)\\_______
         (__)\\        )\\/\\
              ||----w |
              ||     ||"""


class TestCow(unittest.TestCase):
    """Tests the cow command."""

    def test_cow(self):
        """
        Tests the cow command.
        """

        self.assertEqual(makevalidcow("123"), ergo("cow 123"))
        self.assertEqual(makevalidcow("abcabcabc"), ergo("cow abcabcabc"))

