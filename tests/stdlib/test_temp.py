#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_temp.py]

Tests the temp command.
"""

import os
import unittest

from ergonomica.ergo import ergo

class TestTemp(unittest.TestCase):
    """Tests the temp command."""    

    def test_temp(self):
        """
        Tests the temp command.
        """
        
        self.assertTrue(os.path.isfile(ergo("temp file")))
        self.assertTrue(os.path.isdir(ergo("temp dir")))
