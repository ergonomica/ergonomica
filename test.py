#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[test.py]

Unittests for Ergonomica.
"""

import unittest
from ergonomica import ergo
from lib.lang.ergo2bash import ergo2bash
import os
import sys
import subprocess

class TestStringMethods(unittest.TestCase):

    def test_mixed_quotes(self):
        """
        "Single quotes between double quotes not parsing correctly"
        @lschumm
        https://github.com/ergonomica/ergonomica/issues/17
        """
        
        self.assertEqual(ergo("echo \"hello 'world'\""), ["hello 'world'"])

    def test_ergo2bash(self):
        """
        "ergo2bash not working properly for arguments"
        @lschumm
        https://github.com/ergonomica/ergonomica/issues/26
        """

        self.assertEqual(ergo2bash("a b c {d:t} {e:test}").replace("  "," "), "a b c -d -e test")

    def test_lonely_operator(self):
        """
        "Lonely (valid) operators returning OperatorError"
        https://github.com/ergonomica/ergonomica/issues/16
        """
        self.assertNotEqual(ergo("(map)"), ["[ergo: OperatorError]: No such operator 'map'."])

    def test_addline(self):
        """
        Test the addline command.
        """
        open("test-addline", "w")
        ergo('addline "TESTING this feature\n" "once again testing this feature" {file:test-addline}')
        self.assertEqual(open("test-addline", "r").readlines(), ["TESTING this feature\n", "once again testing this feature"])

    #def test_addline_with_no_input(self): 

    def test_alias(self):
        """
        Test the alias command.
        """
        ergo('alias LIST_THEM_FILES ls')

        self.assertEqual(ergo("LIST_THEM_FILES"), ergo("ls"))

    def test_bash(self):
        """
        Test the bash command.
        """
        print("b", ergo('bash "echo -n test"'))
        
        self.assertEqual(ergo('bash "echo -n test"'), ["test"]) 
    
    
if __name__ == '__main__':

    try:
        os.mkdir("ergonomica-test")
        os.chdir("ergonomica-test")
    except:
        pass
    
    unittest.main()
    os.rmdir("ergonomica-test")
