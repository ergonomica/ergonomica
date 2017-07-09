"""
[tests/function_definition.py]

Test the definition of functions in Ergonomica.
"""

import unittest
from ergonomica.ergo import ergo
import random

class TestNestedExpressions(unittest.TestCase):
    """Test that nested expressions work properly."""

    def test_arbitary_number_of_expressions(self):
        """Test nested expressions of an arbitrary (large) number."""

        depth = random.randint(1, 250)
        command = "print "
        command += "$(print " * depth
        command += "123"
        command += ")" * depth
        self.assertEqual(ergo(command), [['123']])


if __name__ == '__main__':
    unittest.main()
