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
    

    def test_get_set(self):
        """
        Tests the get and set commands.
        """
        ergo("set lol_this_is_a_random_variable_name 1337")
        self.assertEqual(ergo("get lol_this_is_a_random_variable_name"), "1337")

    def test_length(self):
        """
        Tests the length command.
        """
        self.assertEqual(ergo("length 1 2 3"), "3")

    #def test_load_config(self):

    def test_ls(self):
        """
        Tests the ls command.
        """
        self.assertEqual(ergo("ls"), os.listdir("."))

    def test_macro(self):
        """
        Tests the macro command.
        """
        ergo("macro lolwut wut")
        self.assertEqual(ergo("echo lolwut"), ergo("echo wut"))

    def test_mkdir(self):
        """
        Tests the mkdir command.
        """
        os.rmdir("test-mkdir")
        ergo("mkdir test-mkdir")
        b = False
        try:
            os.mkdir("test-mkdir")
        except OSError:
            b = True
        self.assert_(b)

    def test_multiply(self):
        """
        Tests the multiply command.
        """
        self.assertEqual(ergo("multiply 1 2 3 {num:2}"), [1,2,3,1,2,3))

    def test_mv(self):
        """
        Tests the mv command.
        """
        os.chdir("ergonomica-test")
        open("test-mv", "w").write("test")
        ergo("mv test-mv test-mv-2")
        self.assertEqual(open("test-mv-2", "r").read(), "test")

    def test_nequal(self):
        """
        Tests the nequal command.
        """
        self.assertEqual(ergo("nequal 1 2"), True)

    #def test_ping(self):

    def test_pwd(self):
        """
        Tests the pwd command.
        """
        self.assertEqual(ergo("pwd"), os.curdir())
        
    #def test_python(self):

    #def test_quit(self):

    def test_read(self):
        """
        Tests the read command.
        """

        os.chdir("ergonomica-test")
        open("test-read", "w").write("we are number one")
        self.assertEqual(ergo("read test-read"), "we are number one")

    def test_removeline(self):
        """
        Tests the readline command.
        """
        os.chdir("ergonomica-test")
        open("test-removeline", "w").writelines(["a", "b", "c"])
        ergo("removeline 0 2 test-removeline")
        self.assertEqual(ergo("read test-removeline"), ["b"])

    def test_rm(self):
        """
        Tests the rm command.
        """
        os.chdir("ergonomica-test")
        open("test-rm", "w")
        ergo("rm test-rm")
        b = False
        try:
            open("test-rm", "r")
        except OSError:
            b = True
        self.assert_(b)

    def test_rmtree(self):
        """
        Tests the rmtree command.
        """

        
    
if __name__ == '__main__':

    try:
        os.mkdir("ergonomica-test")
        os.chdir("ergonomica-test")
    except:
        pass
    
    unittest.main()
    os.rmdir("ergonomica-test")
