"""
[tests/stdlib/test_help.py]

Test the help command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestAddstring(unittest.TestCase):
    """Tests the `addstring` command."""

    def test_list_commands(self):
        self.assertEqual("help commands")
        
        
        
    def test_help_command(self):

        self.assertEqual("help command")
        