#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_pwd.py]

Tests the pwd command.
"""

import os
import unittest
from ergonomica import ergo

class TestPwd(unittest.TestCase):
    """Tests the pwd command."""

    def test_pwd(self):
        """
        Tests the pwd command.
        """

        self.assertEqual(ergo("pwd"), os.getcwd())
