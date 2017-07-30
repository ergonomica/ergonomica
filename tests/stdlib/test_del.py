#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_del.py]

Test the del command.
"""

import unittest
import os

from ergonomica.ergo import ergo

class TestDel(unittest.TestCase):
    """Tests the del command."""

    def test_del_variable(self):
        """
        Tests the del function on a user-defined variable.
        """
        
        # create the variable
        ergo("set x 2")
        
        # delete it
        ergo("del x")
        
        # check that it's not still in the namespace
        self.assertEqual(ergo("get x"), [])
        
    def test_del_multiple_variables(self):
        """
        Tests the del function on multiple user-defined variables.
        """
        
        # create the variables
        ergo("set x 2")
        ergo("set y 242246")
        ergo("set z agw409ua09ig0")
        
        # delete the variables
        ergo("del x")
        ergo("del y")
        ergo("del z")
        
        # check that they're not still in the namespace
        self.assertEqual(ergo("get x"), [])
        self.assertEqual(ergo("get y"), [])
        self.assertEqual(ergo("get z"), [])
                

    def test_del_function(self):
        """
        Tests the del function on a user-defined function.
        """

        # create the function
        ergo("def f\n   print c")
        
        # delete it
        ergo("del f")
        
        # check that it's not still in the namespace
        self.assertEqual(ergo("get f"), [])

    def test_del_multiple_functions(self):
        """
        Tests the del function on multiple user-defined functions.
        """

        # create the functions
        ergo("def f\n   print c")
        ergo("def g\n   print c")

        
        # delete them
        ergo("del f")
        ergo("del g")
        
        # check that they're not still in the namespace
        self.assertEqual(ergo("get f"), [])
        self.assertEqual(ergo("get g"), [])
