#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[test.py]

Unittests for Ergonomica.
"""

import unittest
import os
import pytest
import sys

from ergonomica.ergo import ergo
from ergonomica.lib.lang.ergo2bash import ergo2bash
from ergonomica.lib.lang.error import ErgonomicaError
import shutil
import subprocess


def mkdir_force(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


from ergonomica.lib.lang.environment import Environment

ENV = Environment()

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

        try:
            ergo("(map)")
        except Exception as error:
            self.assertNotEqual(str(error), ["[ergo: OperatorError]: No such operator 'map'."])

    def test_addline(self):
        """
        Test the addline command.
        """
        open("test-addline", "w")
        ergo('addline "TESTING this feature\n" "once again testing this feature" {file:"test-addline"}')
        self.assertEqual(open("test-addline", "r").readlines(), ["TESTING this feature\n", "once again testing this feature"])

    #def test_addline_with_no_input(self):

    def test_alias(self):
        """
        Test the alias command.
        """
        ergo('alias LIST_THEM_FILES ls')

        self.assertEqual(ergo("LIST_THEM_FILES"), ergo("ls"))

    # def test_bash(self):
    #     """
    #     Test the bash command.
    #     """

    #     self.assertEqual(ergo('bash "echo -n test"'), ["test"])

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
        try:
            ergo("rm test-cp-2")
        except:
            pass
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
        self.assertEqual(ergo("help echo"), "echo [STRING,...] {ind:[INT,...]} |  "
                                            "Prints its input. If ind specified, returns the items of its input with the specified indices.\n\n"
                                            "Visit https://github.com/ergonomica/ergonomica/wiki for more documentation.")

    #def text_export(self):

    # def test_find(self):
    #     """
    #     Tests the find command.
    #     """

    #     try:
    #         os.mkdir("test-find")
    #     except OSError:
    #         pass
    #     os.chdir("test-find")
    #     for i in ["a_test_this_is.vba","a_cool_code.asm","this_doesnt_match.md"]:
    #         open(i, "w")
    #     self.assertEqual(ergo("find {name:a.*a}"), ["a_test_this_is.vba","a_cool_code.asm"])

    #def test_fish(self):

    #def test_free(self):


    def test_get_set(self):
        """
        Tests the get and set commands.
        """
        ergo("set {lol_this_is_a_random_variable_name:1337}")
        self.assertEqual(ergo("get lol_this_is_a_random_variable_name"), [1337])

    def test_length(self):
        """
        Tests the length command.
        """
        self.assertEqual(ergo("length"), 0)
        self.assertEqual(ergo("length 1 2 3"), 3)

    #def test_load_config(self):

    def test_ls(self):
        """
        Tests the ls command.
        """
        self.assertEqual(ergo("ls"), [ENV.theme["files"] + x for x in os.listdir(".")])

        mkdir_force("ls_dir_test")
        self.assertEqual(ergo("ls ls_dir_test"), ["ls_dir_test:"])

        open("ls_dir_test/file1", 'w+')
        open("ls_dir_test/file2", 'w+')
        self.assertEqual(ergo("ls ls_dir_test"),
                         ["ls_dir_test:"] + [ENV.theme["files"] + x for x in os.listdir("ls_dir_test")])

        mkdir_force("ls_dir_test2")
        open("ls_dir_test2/file1", 'w+')
        open("ls_dir_test2/file2", 'w+')
        self.assertEqual(ergo("ls ls_dir_test ls_dir_test2"),
                         ["ls_dir_test:"] + [ENV.theme["files"] + x for x in os.listdir("ls_dir_test")] +
                         ["ls_dir_test2:"] + [ENV.theme["files"] + x for x in os.listdir("ls_dir_test2")])

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
        if os.path.isdir("mkdir_test"):
            os.rmdir("mkdir_test")
        ergo("mkdir mkdir_test")
        self.assertTrue(os.path.isdir("mkdir_test"))

        error_dir_exist = False
        mkdir_force("mkdir_test2")
        try:
            ergo('mkdir mkdir_test2')
        except:
            error_dir_exist = True
        self.assertTrue(error_dir_exist)

        error_dir_exist_overwrite = False
        mkdir_force("mkdir_test3")
        open("mkdir_test3/file1", "w+")  # test if folder was overwritten
        try:
            ergo('mkdir mkdir_test3 {overwrite:"true"}')
        except:
            error_dir_exist_overwrite = True
        self.assertFalse(error_dir_exist_overwrite)
        self.assertEqual(os.listdir("mkdir_test3"), [])


    def test_multiply(self):
        """
        Tests the multiply command.
        """
        self.assertEqual(ergo("multiply 1 2 3 {num:2}"), ['1','2','3','1','2','3'])

    # def test_mv(self):
    #     """
    #     Tests the mv command.
    #     """

    #     s = open("test-mv", "w")
    #     s.write("test")
    #     s.close()
    #     ergo("mv test-mv test-mv-2")
    #     self.assertEqual(open("test-mv-2", "r").read(), "test")

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
        self.assertEqual(ergo("pwd"), os.getcwd())

    #def test_python(self):

    #def test_quit(self):

    def test_read(self):
        """
        Tests the read command.
        """
        open("test-read", "w").write("we are number one")
        self.assertEqual(ergo("read test-read"), ["we are number one"])

    # def test_removeline(self):
    #     """
    #     Tests the readline command.
    #     """

    #     open("test-removeline", "w").writelines(["a\n", "b\n", "c\n"])
    #     ergo("removeline 0 2 test-removeline")
    #     self.assertEqual(ergo("read test-removeline"), ["b"])

    def test_rm(self):
        """
        Tests the rm command.
        """
        open("test-rm", "w")
        ergo("rm test-rm")
        self.assertFalse(os.path.exists("test-rm"))

        mkdir_force("test_dir_rm")
        ergo("rm test_dir_rm")
        self.assertFalse(os.path.exists("test_dir_rm"))

        if (os.path.exists("rm_not_exist")):
            os.remove("rm_not_exist")
        with pytest.raises(Exception):
            ergo("rm rm_not_exist")


    #def test_shuffle(self):

    def test_size(self):
        f = open("test_size", "w+")
        f.write("some bytes")
        f.flush()
        self.assertTrue(str(os.path.getsize("test_size")) in ergo('size test_size {unit:"B"}')[0])

        mkdir_force("size_dir")
        mkdir_force("size_dir/inner_dir")
        f1 = open("size_dir/test_size", "w+")
        f1.write("some bytes")
        f1.flush()
        f2 = open("size_dir/inner_dir/test_size", "w+")
        f2.write("some other bytes")
        f2.flush()
        self.assertTrue(str(os.path.getsize("size_dir/test_size") + os.path.getsize("size_dir/inner_dir/test_size")) in
                        ergo('size size_dir {unit:"B"}')[0])

    # def test_sort(self):
    #     """
    #     Tests the sort command.
    #     """

    #     try:
    #         os.mkdir("test-sort")
    #     except OSError:
    #         pass
    #     os.chdir("test-sort")
    #     for i in ["a.txt", "abel.txt", "annie.txt", "beth.txt"]:
    #         open(i, "w")
    #     ergo("sort {exp:.}")
    #     self.assert_(os.exists("./a/a.txt") and os.path.exists("./a/abel.txt") and os.path.exists("./a/annie.txt") and os.path.exists("./b/beth.txt"))

    #def test_string_find(self):

    # def test_swap(self):
    #     """
    #     Tests the swap command.
    #     """

    #     try:
    #         os.rmdir("test-swap")
    #     except OSError:
    #         pass
    #     os.mkdir("test-swap")
    #     os.chdir("test-swap")
    #     open("a.txt", "w").write("a")
    #     open("b.txt", "w").write("b")
    #     ergo("swap a.txt b.txt")
    #     self.assertEqual([open("a.txt", "r").read(), open("b.txt", "r").read()], [["b"], ["a"]])

    #def test_title(self):

    #def test_users(self):

    def test_version(self):
        """
        Tests the version command.
        """

        self.assertEqual(ergo("version"), "Ergonomica &&&VERSION&&&.")

    #def test_weather(self):

    def test_whoami(self):
        """
        Tests the whoami command.
        """

        self.assertEqual(ergo("whoami"), os.environ["USER"])

    def test_yes(self):
        """
        Tests the yes command.
        """

        self.assertEqual(ergo("yes"), "y\n")


    #def test_zsh(self):

if __name__ == '__main__':

    try:
        os.mkdir("ergonomica-test")

    except:
        pass

    unittest.main()
    os.rmdir("ergonomica-test")
