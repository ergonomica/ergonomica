"""
[test.py]

Unittests for Ergonomica.
"""
import unittest
import os
from os import mkdir
import pytest
import sys
from ergonomica.ergo import evaluate
from ergonomica.lib.lang.ergo2bash import ergo2bash
from ergonomica.lib.lang.error import ErgonomicaError
import shutil
import subprocess

from ergonomica.lib.lang.environment import Environment
ENV = Environment()

class TestStringMethods(unittest.TestCase):

    def test_mixed_quotes(self):
        """
        "Single quotes between double quotes not parsing correctly"
        @lschumm
        https://github.com/ergonomica/ergonomica/issues/17
        """
        self.assertEqual(evaluate('echo "hello \'world\'"'), ["hello 'world'"])

    def test_ergo2bash(self):
        """
        "ergo2bash not working properly for arguments"
        @lschumm
        https://github.com/ergonomica/ergonomica/issues/26
        """
        self.assertEqual(ergo2bash('a b c {d:t} {e:test}').replace('  ', ' '), 'a b c -d -e test')

    def test_lonely_operator(self):
        """
        "Lonely (valid) operators returning OperatorError"
        https://github.com/ergonomica/ergonomica/issues/16
        """
        try:
            evaluate('(map)')
        except Exception as error:
            self.assertNotEqual(str(error), ["[ergo: OperatorError]: No such operator 'map'."])

    def test_addline(self):
        """
        Test the addline command.
        """
        open('test-addline', 'w')
        evaluate('addline "TESTING this feature" "once again testing this feature" {file:"test-addline"}')
        self.assertEqual(open('test-addline', 'r').readlines(), ['TESTING this feature\n', 'once again testing this feature\n'])

    def test_alias(self):
        """
        Test the alias command.
        """
        evaluate('alias LIST_THEM_FILES ls')
        self.assertEqual(evaluate('LIST_THEM_FILES'), evaluate('ls'))

    def test_cd(self):
        """
        Test the cd command.
        """
        original = evaluate('pwd')
        try:
            os.mkdir('test-cd')
        except OSError:
            pass

        evaluate('cd test-cd')
        self.assertEqual(original + '/test-cd', evaluate('pwd'))

    def test_cp(self):
        """
        Test the cp command.
        """
        try:
            evaluate('rm test-cp-2')
        except:
            pass

        open('test-cp-1', 'w')
        evaluate('cp test-cp-1 test-cp-2')
        self.assert_('test-cp-2' in os.listdir('.'))

    def test_echo(self):
        """
        Test the echo command.
        """
        self.assertEqual(evaluate('echo hello there'), ['hello', 'there'])

    def test_equal(self):
        """
        Test the equal command.
        """
        self.assertEqual(evaluate('equal 1 1') and evaluate('equal 1 2'), False)

    def test_help(self):
        """
        Test the help command.
        """
        self.assertEqual(evaluate('help echo'), 'echo [STRING,...] {ind:[INT,...]} |  Prints its input. If ind specified, returns the items of its input with the specified indices.\n\nVisit https://github.com/ergonomica/ergonomica/wiki for more documentation.')

    def test_get_set(self):
        """
        Tests the get and set commands.
        """
        evaluate('set {lol_this_is_a_random_variable_name:1337}')
        self.assertEqual(evaluate('get lol_this_is_a_random_variable_name'), [1337])

    def test_length(self):
        """
        Tests the length command.
        """
        self.assertEqual(evaluate('length'), 0)
        self.assertEqual(evaluate('length 1 2 3'), 3)

    def test_ls(self):
        """
        Tests the ls command.
        """
        self.assertEqual(evaluate('ls'), [ ENV.theme['files'] + x for x in os.listdir('.') ])
        mkdir('ls_dir_test')
        self.assertEqual(evaluate('ls ls_dir_test'), ['ls_dir_test:'])
        open('ls_dir_test/file1', 'w+')
        open('ls_dir_test/file2', 'w+')
        self.assertEqual(evaluate('ls ls_dir_test'), [
         'ls_dir_test:'] + [ ENV.theme['files'] + x for x in os.listdir('ls_dir_test') ])
        mkdir('ls_dir_test2')
        open('ls_dir_test2/file1', 'w+')
        open('ls_dir_test2/file2', 'w+')
        self.assertEqual(evaluate('ls ls_dir_test ls_dir_test2'), [
         'ls_dir_test:'] + [ ENV.theme['files'] + x for x in os.listdir('ls_dir_test') ] + ['ls_dir_test2:'] + [ ENV.theme['files'] + x for x in os.listdir('ls_dir_test2') ])

    def test_macro(self):
        """
        Tests the macro command.
        """
        evaluate('macro lolwut wut')
        self.assertEqual(evaluate('echo lolwut'), evaluate('echo wut'))

    def test_mkdir(self):
        """
        Tests the mkdir command.
        """
        if os.path.isdir('mkdir_test'):
            os.rmdir('mkdir_test')
            evaluate('mkdir mkdir_test')
            self.assertTrue(os.path.isdir('mkdir_test'))
        error_dir_exist = False
        mkdir('mkdir_test2')
        try:
            evaluate('mkdir mkdir_test2')
        except:
            error_dir_exist = True
            self.assertTrue(error_dir_exist)

        error_dir_exist_overwrite = False
        mkdir('mkdir_test3')
        open('mkdir_test3/file1', 'w+')
        try:
            evaluate('mkdir mkdir_test3 {overwrite:"true"}')
        except:
            error_dir_exist_overwrite = True
            self.assertFalse(error_dir_exist_overwrite)
            self.assertEqual(os.listdir('mkdir_test3'), [])

    def test_multiply(self):
        """
        Tests the multiply command.
        """
        self.assertEqual(evaluate('multiply 1 2 3 {num:2}'), ['1', '2', '3', '1', '2', '3'])

    def test_nequal(self):
        """
        Tests the nequal command.
        """
        self.assertEqual(evaluate('nequal 1 2'), True)

    def test_pwd(self):
        """
        Tests the pwd command.
        """
        self.assertEqual(evaluate('pwd'), os.getcwd())

    def test_read(self):
        """
        Tests the read command.
        """
        open('test-read', 'w').write('we are number one')
        self.assertEqual(evaluate('read test-read'), ['we are number one'])

    def test_rm(self):
        """
        Tests the rm command.
        """
        open('test-rm', 'w')
        evaluate('rm test-rm')
        self.assertFalse(os.path.exists('test-rm'))
        mkdir('test_dir_rm')
        evaluate('rm test_dir_rm')
        self.assertFalse(os.path.exists('test_dir_rm'))
        if os.path.exists('rm_not_exist'):
            os.remove('rm_not_exist')
        with pytest.raises(Exception):
            evaluate('rm rm_not_exist')

    def test_size(self):
        f = open('test_size', 'w+')
        f.write('some bytes')
        f.flush()
        self.assertTrue(str(os.path.getsize('test_size')) in evaluate('size test_size {unit:"B"}')[0])
        mkdir('size_dir')
        mkdir('size_dir/inner_dir')
        f1 = open('size_dir/test_size', 'w+')
        f1.write('some bytes')
        f1.flush()
        f2 = open('size_dir/inner_dir/test_size', 'w+')
        f2.write('some other bytes')
        f2.flush()
        self.assertTrue(str(os.path.getsize('size_dir/test_size') + os.path.getsize('size_dir/inner_dir/test_size')) in evaluate('size size_dir {unit:"B"}')[0])

    def test_version(self):
        """
        Tests the version command.
        """
        self.assertEqual(evaluate('version'), 'Ergonomica &&&VERSION&&&.')

    def test_whoami(self):
        """
        Tests the whoami command.
        """
        self.assertEqual(evaluate('whoami'), os.environ['USER'])

    def test_yes(self):
        """
        Tests the yes command.
        """
        self.assertEqual(evaluate('yes'), 'y\n')


if __name__ == '__main__':
    try:
        os.mkdir('ergonomica-test')
    except:
        pass

    unittest.main()
    os.rmdir('ergonomica-test')
