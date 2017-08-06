#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_rprompt.py]

Tests the rprompt command.
"""

import unittest

from ergonomica.ergo import ergo

class TestBuiltins(unittest.TestCase):
    """Tests the builtins."""

    def test_print(self):
        """
        Tests that the print command works properly.
        """
        
        self.assertEqual("print 1", 1)
        self.assertEqual("print 2 2", [2, 2])
        
    def test_sleep(self):
        """
        Tests that the sleep command works properly.
        """
        
        # just test if it runs
        ergo("sleep 13")

    def test_add(self):
        """
        Tests that + (the addition command) works properly.
        """
        
        self.assertEqual(ergo("+ 3 3 3", 9))
        self.assertCountEqual(ergo("+ (list 1 3 5) (list 2 4 6)"), [1, 2, 3, 4, 5, 6])
        self.assertEqual(ergo("+ stringa stringb"), "stringastringb")

    def test_subtraction(self):
        """
        Tests that - (the subtraction command) works properly.
        """
        
        self.assertEqual(ergo("- 3 2"), 1)

    def test_exponentiation(self):
        """
        Tests that ^ (the exponentiation command) works properly.
        """

        self.assertEqual(ergo("^ 3 2"), 9)

    def test_division(self):
        """
        Test that / (the division command) works properly.
        """
        
        self.assertEqual(ergo("/ 3 2"), 1.5)

    def test_leq(self):
        """
        Tests that <= (the less than or equal to command) works properly.
        """

        self.assertFalse("<= 4 3")
        self.assertTrue("<= 3 3")

    def test_lessthan(self):
        """
        Tests that < (the less than command) works properly.
        """

        self.assertFalse("< 3 2")
        self.assertTrue("< 2 100")
        
        
    def test_greaterthan(self):
        """
        Tests that > (the greater than command) works properly.
        """

        self.assertTrue("> 3 2")
        self.assertFalse("> 3 3")

        
    def test_geq(self):
        """
        Tests that >= (the greater than or equal to command) works properly.
        """
        
        self.assertTrue(">= 3 2")
        self.assertFalse(
        

    def test_multiplication(self):
        """
        Tests that * (the multiplication command) works properly.
        """

        self.assertEqual(ergo("* 9 6"), 54)
        self.assertEqual(ergo("* abc 3"), "abcabcabc")
        self.assertEqual(ergo("* (list 1) 3"), [1, 1, 1])

    def test_true(self):
        """
        Tests that #t has the correct value.
        """

        self.assertEqual(ergo("#t"), True)

    def test_false(self):
        """
        Tests that #f has the correct value.
        """
        
        self.assertEqual(ergo("#f"), False)

    def test_none(self):
        """
        Tests that #none (just Python's None) has the correct value.
        """
        
        self.assertEqual(ergo("#none"), None)

    
    def test_pi(self):
        """
        Tests that #pi has the correct value.
        """
        
        self.assertEqual(ergo("#pi"), 3.141592653589793)

    def test_e(self):
        """
        Tests that #e (Euler's constant) has the correct value.
        """

        self.assertEqual(ergo("#e"), 2.718281828459045)

    def test_j(self):
        """
        Tests that #j (the imaginary unit) has the correct value.
        """

        self.assertEqual(ergo("#j"), 1j)

    def test_equal(self):
        """
        Tests that = (the equal function) works properly.
        """

        self.assertTrue("= (list 1 2) (list 1 2)")
        self.assertFalse("= abababa 33.0")
        

    def test_nequal(self):
        """
        Tests that != (the not equal function) works properly.
        """

        self.assertTrue("!= 3 9 9 4")
        self.assertFalse("!= string string string")
        
    def test_type(self):
        """
        Tests that the type function works properly.
        """

        self.assertEqual(ergo("type 1"), "int")
        self.assertEqual(ergo("type 4.096"), "float")
        self.assertEqual(ergo("type string"), "str")
        self.assertEqual(ergo("type (list 1 2 3)"), "list")


    def test_pipe(self):
        """
        Tests that the pipe function works properly.
        """

        self.assertEqual(ergo("print 1 2 3 | first {}"), [1])
        self.assertEqual(ergo("print 4 9 2 | print {0}"), [4, 9, 2])
        self.assertEqual(ergo("print 2 4 6 8 | print {1}"), [4, 8])
        self.assertEqual(ergo("print 2 4 6 8 | print {0/1}"), [2, 6])
        
        
    def test_first(self):
        """
        Tests that the first function works properly.
        """

        self.assertEqual(ergo("first (list 4 9 6)"), 4)
        
        
    def test_rest(self):
        """
        Tests that the rest function works properly.
        """

        self.assertCountEqual(ergo("rest (list 4 9 6)"), [9, 6])
            
        
    def test_list(self):
        """
        Tests that the list function works properly.
        """

        self.assertCountEqual(ergo("list 4 9 a 3 (list 3)", [4, 9, "a", 3, [3]])


    def test_split(self):
        """
        Tests that the split function works properly.
        """

        self.assertCountEqual(ergo("split 1,2,3 ,"), [1,2,3])

                              
    def test_flatten(self):
        """
        Tests that the flatten function works properly.
        """

        self.assertCountEqual(ergo("flatten (list (list 1 2 (list 3)) 4 5)"), [1, 2, 3, 4, 5])

                              
    def test_zip(self):
        """
        Tests that the zip function works properly.
        """
        
        self.assertCountEqual(ergo("zip (list 1 2 3) (list 4 5 6)"), [1, 2, 3, 4, 5, 6])
        self.assertCountEqual(ergo("zip abc def"), ["a", "d", "b", "e", "c", "f"])
        

    def test_apply(self):
        """
        Tests that the apply function works properly.
        """

        self.assertEqual("apply $= (list 1 2 3)", False)
        self.assertEqual("apply $+ (list a b c)", "abc")

    # no easy way of checking if these are random---
    # see https://xkcd.com/221/

    def test_random(self):
        """
        Tests that the random function works properly.
        """

        value = ergo("random")
        self.assertTrue((0 < value) and (1 > value))
    
    def test_randint(self):
        """
        Tests that the randint function works properly.
        """

        value1 = ergo("randint 10")
        value2 = ergo("randint 50 60")

        self.assertTrue((0 <= value1) and (10 >= value1))
        self.assertTrue((50 <= value2) and (60 >= value2))
        

    def test_randpick(self):
        """
        Tests that the randpick function works properly.
        """
        
        self.assertTrue(ergo("randpick (list 1 2 3)") in [1,2,3])
        

    def test_round(self):
        """
        Tests that the round function works properly.
        """

        self.assertEqual(ergo("round #pi 2"), 3.14)
