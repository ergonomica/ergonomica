#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_rprompt.py]

Tests the rprompt command.
"""

import unittest

from ergonomica.ergo import ergo

class TestRprompt(unittest.TestCase):
    """Tests the rprompt command."""
    
    # NOTE: as of yet, there isn't really a way of testing this,
    # so just check if it throws an exception

    def test_rprompt(self):
        """
        Tests the rprompt command.
        """

        ergo("rprompt 123")
