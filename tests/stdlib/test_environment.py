#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_environment.py]

Tests the environment command.
"""

import os
import unittest

from ergonomica import ergo

class TestEnvironment(unittest.TestCase):
    """Tests the environment command."""

    def test_environment(self):
        """
        Tests the environment command.
        """

        # set a variable
        ergo("environment set prompt 123123123123> ")

        # verify its value
        self.assertEqual(ergo("environment get prompt"), "123123123123>")

