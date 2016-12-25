#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[test.py]

Unittests for Ergonomica.
"""

import unittest
from ergonomica import ergo

class TestStringMethods(unittest.TestCase):

    def test_yes(self):
        self.assertEqual(ergo("echo a"), ['a'])

    def test_echo(self);
    
        
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
