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
        
        self.assertEqual(ergo('bash "echo -n test"'), ["test"])

    def test_cd(self):
        """
        Test the cd command.
        """
        original = ergo("pwd")
        try:
            os.mkdir("test-cd")
        except OSError:
            # directory already exists
            pass
        ergo("cd test-cd")
        self.assertEqual(original + "/test-cd", ergo("pwd")) 

    #def test_clear(self):

    def test_cp(self):
        """
        Test the cp command.
        """
        ergo("rm test-cp-2")
        open("test-cp-1", "w")
        ergo("cp test-cp-1 test-cp-2")
        self.assert_("test-cp-2" in os.listdir("."))

    def test_echo(self):
        """
        Test the echo command.
        """
        self.assertEqual(ergo("echo hello there"), ["hello", "there"])

    #def test_edit(self):

    def test_equal(self):
        """
        Test the equal command.
        """
        self.assertEqual(ergo("equal 1 1") and ergo("equal 1 2"), False)


    def test_help(self):
        """
        Test the help command.
        """
        self.assertEqual(ergo("help echo"), "echo [STRING,...]          |              Prints its input.\n")

    #def text_export(self):

    def test_find(self):
        """
        Tests the find command.
        """
        os.chdir("ergonomica-test")
        try:
            os.mkdir("test-find")
        except OSError:
            pass
        os.chdir("test-find")
        for i in ["a_test_this_is.vba","a_cool_code.asm","this_doesnt_match.md"]:
            open(i, "w")
        self.assertEqual(ergo("find {name:a.*a}"), ["a_test_this_is.vba","a_cool_code.asm"])

    #def test_fish(self):

    #def test_free(self):
    
    
    
        
if __name__ == '__main__':

    try:
        os.mkdir("ergonomica-test")
        os.chdir("ergonomica-test")
    except:
        pass
    
    unittest.main()
    os.rmdir("ergonomica-test")
