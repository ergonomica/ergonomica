"""
[tests/function_definition.py]

Test the definition of functions in Ergonomica.
"""

import unittest
from ergonomica.ergo import ergo


class TestFunctionDefinitions(unittest.TestCase):
    """Test that simple Ergonomica function definitions work."""

    def test_simple_function(self):
        """
        Test that a simple function definition works.
        """
        self.assertEqual(ergo("def f\n    print testing\nf"), ["a"])

    def test_nested_functions(self):
        """
        Test that functions defined inside other functions behave correctly.
        """
        self.assertEqual(ergo("def f\n    def g\n        print testing\n   g\n"), [["testing"]])


if __name__ == '__main__':
    unittest.main()
