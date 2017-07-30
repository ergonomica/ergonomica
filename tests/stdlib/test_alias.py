#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_alias.py]

Test the alias command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestAlias(unittest.TestCase):
    """Tests the alias command."""

    def test_alias_variable(self):
        """
        Tests the del function on a user-defined variable.
        """
        
        # set the variable
        ergo("set x 2")
        
        # set the alias
        ergo("alias y x")
        
        self.assertEqual(ergo("get y"), [2])
        
        # delete the created variables
        ergo("del x y")

        
    def test_alias_user_function(self):
        """
        Tests the alias function on a user-defined function.
        """

        # set the function
        ergo("def f\n   print $(+ 1 2)")
        
        # set the alias
        ergo("alias g f")
        
        # check that the functions output the same value
        self.assertEqual(ergo("f"), ergo("g"))
        
        # delete the created functions
        ergo("del f g")
        
    def test_alias_stdlib_function(self):
        """
        Tests the alias function on a function from the standard library.
        """
        
        # set the alias
        ergo("alias LIST_THEM_FILES ls")
        
        # check that it outputs the same values as the stdlib function
        self.assertEqual(ergo("LIST_THEM_FILES"), ergo("ls"))
        
        # delete the created alias
        ergo("del LIST_THEM_FILES")
