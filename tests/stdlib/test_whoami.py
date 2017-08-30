#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_whoami.py]

Tests the whoami command.
"""

import getpass
import unittest

from ergonomica import ergo

class TestWhoami(unittest.TestCase):
    """Tests the whoami command."""

    def test_whoami(self):
        """
        Tests the whoami command.
        """

        self.assertEqual(ergo("whoami"), getpass.getuser())

