#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_ls.py]

Tests the ls command.
"""

import unittest
import os

from ergonomica import ergo

class TestLs(unittest.TestCase):
    """Tests the ls command."""

    def test_ls(self):
        """
        Tests the ls command.
        """

        self.assertCountEqual(ergo('ls'), os.listdir("."))

