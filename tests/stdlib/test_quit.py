#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_quit.py]

Test the quit command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestQuit(unittest.TestCase):
    """Tests the `ls` command."""

    def test_quit(self):
        """
        Test the quit function.
        """

        self.assertItemsEqual(ergo('ls'), os.listdir("."))
