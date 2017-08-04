#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_py.py]

Tests the py command.
"""

import os
import unittest

from ergonomica.ergo import ergo

class TestPy(unittest.TestCase):
    """Tests the py command."""

    def test_py(self):
        """
        Tests the py command.
        """

        # set a variable in the Ergonomica namespace
        ergo("set l 2")

        # use it in a Python expression
        self.assertEqual(ergo("py \"l + 2\""), 4)

        # delete the variable after use
        ergo("del l")

