"""
[tests/function_definition.py]

Test the definition of functions in Ergonomica.
"""

import unittest
from ergonomica.ergo import ergo
import random, string

def randomword(length):
    length = random.choice(range(length))
    return ''.join(random.choice(string.lowercase) for i in range(length))

class TestStringMethods(unittest.TestCase):

    def test_simple_function(self):
        """
        Test that a simple function definition works.
        """
        self.assertEqual(ergo("def f\n    print %s\nf" % randomword()) , ["a"]) 

    def test_nested_functions(self):
        """
        Test that functions defined inside other functions behave correctly.
        """
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
