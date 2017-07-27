#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_help.py]

Test the help command.
"""

import unittest
import os

from ergonomica.ergo import ergo, ENV

class TestHelp(unittest.TestCase):
    """Tests the 'help' command."""

    def test_list_commands(self):
        """
        Tests listing all commands using the 'help commands' command.
        """
        
        self.assertItemsEqual(ergo("help commands"), [k for k in ENV.ns if callable(ENV.ns[k])])
        
    def test_help_commands(self):
        """
        Tests that 'help command' properly returns the docstring of functions.
        """
        
        for k in ENV.ns:
            self.assertEqual(ergo("help command {}".format(k)), [ENV.ns[k].__doc__])
