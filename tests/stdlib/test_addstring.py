#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_addstring.py]

Test the addstring command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestAddstring(unittest.TestCase):
    """Tests the `addstring` command."""

    def test_addstring(self):
        """
        Test the addstring function.
        """
        
        self.assertEqual(ergo("print oq4ij 4ojioj1iorj oo4joijoi12' | addstring"), ["oq4ij4ojioj1iorjoo4joijoi12'"])
