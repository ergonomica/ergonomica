#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_del.py]

Test the del command.
"""

import unittest

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
        self.assertEqual(ergo("get x"), None)
        
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
        self.assertEqual(ergo("get x"), None)
        self.assertEqual(ergo("get y"), None)
        self.assertEqual(ergo("get z"), None)
