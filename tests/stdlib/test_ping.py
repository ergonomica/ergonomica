#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_ping.py]

Tests the ping command.
"""

import unittest

from ergonomica import ergo

class TestPing(unittest.TestCase):
    """Tests the ping command."""
    
    # NOTE: as of yet, there isn't really a way of testing this,
    # (other than reimplementing) so just check if it throws an exception

    def test_ping(self):
        """
        Tests the ping command.
        """

        ergo("ping aaaaaaaaaaaaaaa") # will say its down
                                     # (won't throw exception)
        ergo("ping -c 2 8.8.8.8 google.com")
        
