"""
[tests/stdlib/test_map.py]

Test the map command.
"""

import unittest
import os

from ergonomica.ergo import ergo


class TestMap(unittest.TestCase):
    """Tests the `map` command."""

    def test_simple_map(self):
        """
        Test the simple application of a function to some input.
        """

        self.assertEqual(ergo('print 1 3 4 | map print {}'), ['1', '3', '4'])


    def test_doublebrackets_same_as_0(self):
        """
        Test that {} performs the same as {0}.
        """

        self.assertEqual(ergo('print 1 2 | map print {} {}'), ergo('print 1 2 | map print {0} {0}'))
        
    def test_interlacing_print(self):
        """
        Test mixing print messages with map format arguments.
        """

        self.assertEqual(ergo('print 1 2 3 4 | map print {0} 3 {1}'), ['1', '3', '2', '3', '3', '4'])
        
    def test_map_shell(self):
        """
        Test mapping a shell function to the output of an Ergonomica function's output.
        """

        self.assertEqual(ergo('print 1 a b 9 \' | map echo {}'), ['1', 'a', 'b', '9', '\''])