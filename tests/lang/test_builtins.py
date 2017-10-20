#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_rprompt.py]

Tests the rprompt command.
"""

import unittest

from ergonomica import ergo

class TestBuiltins(unittest.TestCase):
    """Tests the builtins."""

    def test_print(self):
        """
        Tests that the print command works properly.
        """

        self.assertEqual(ergo("print 1"), 1)
        self.assertEqual(ergo("print 2 2"), [2, 2])

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
        self.assertEqual(set(ergo("+ (list 1 3 5) (list 2 4 6)")), {1, 2, 3, 4, 5, 6})
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

        self.assertFalse(ergo("<= 4 3"))
        self.assertTrue(ergo("<= 3 3"))

    def test_lessthan(self):
        """
        Tests that < (the less than command) works properly.
        """

        self.assertFalse(ergo("< 3 2"))
        self.assertTrue(ergo("< 2 100"))


    def test_greaterthan(self):
        """
        Tests that > (the greater than command) works properly.
        """

        self.assertTrue(ergo("> 3 2"))
        self.assertFalse(ergo("> 3 3"))


    def test_geq(self):
        """
        Tests that >= (the greater than or equal to command) works properly.
        """

        self.assertTrue(ergo(">= 3 2"))
        self.assertTrue(ergo(">= 3 3"))
        self.assertFalse(ergo(">= 3 4"))


    def test_multiplication(self):
        """
        Tests that * (the multiplication command) works properly.
        """

        self.assertEqual(ergo("* 9 6"), 54)
        self.assertEqual(ergo("* abc 3"), "abcabcabc")
        self.assertEqual(ergo("* (list 1) 3"), [1, 1, 1])

    def test_true(self):
        """
        Tests that $t has the correct value.
        """

        self.assertEqual(ergo("print $t"), True)

    def test_false(self):
        """
        Tests that $f has the correct value.
        """

        self.assertEqual(ergo("print $f"), False)

    def test_none(self):
        """
        Tests that #none (just Python's None) has the correct value.
        """

        self.assertEqual(ergo("print $none"), None)


    def test_pi(self):
        """
        Tests that $pi has the correct value.
        """

        self.assertEqual(ergo("print $pi"), 3.141592653589793)

    def test_e(self):
        """
        Tests that #e (Euler's constant) has the correct value.
        """

        self.assertEqual(ergo("print $e"), 2.718281828459045)

    def test_j(self):
        """
        Tests that #j (the imaginary unit) has the correct value.
        """

        self.assertEqual(ergo("print $j"), 1j)

    def test_and(self):
        """
        Tests that the and function works properly.
        """

        self.assertTrue(ergo("and $t $t"))
        self.assertFalse(ergo("and $t $f"))
        self.assertFalse(ergo("and $f $t"))
        self.assertFalse(ergo("and $f $f"))

    def test_or(self):
        """
        Tests that the or function works properly.
        """

        self.assertTrue(ergo("or $t $t"))
        self.assertTrue(ergo("or $t $f"))
        self.assertTrue(ergo("or $f $t"))
        self.assertFalse(ergo("or $f $f"))

    def test_nor(self):
        """
        Tests that the nor function works properly.
        """

        self.assertFalse(ergo("nor $t $t"))
        self.assertFalse(ergo("nor $t $f"))
        self.assertFalse(ergo("nor $f $t"))
        self.assertTrue(ergo("nor $f $f"))

    def test_and(self):
        """
        Tests that the nand function works properly.
        """

        self.assertFalse(ergo("nand $t $t"))
        self.assertTrue(ergo("nand $t $f"))
        self.assertTrue(ergo("nand $f $t"))
        self.assertTrue(ergo("nand $f $f"))

    def test_xor(self):
        """
        Tests that the xor function works properly.
        """

        self.assertFalse(ergo("xor $t $t"))
        self.assertTrue(ergo("xor $t $f"))
        self.assertTrue(ergo("xor $f $t"))
        self.assertFalse(ergo("xor $f $f"))

    def test_equal(self):
        """
        Tests that = (the equal function) works properly.
        """

        self.assertTrue(ergo("= (list 1 2) (list 1 2)"))
        self.assertFalse(ergo("= abababa 33.0"))

    def test_nequal(self):
        """
        Tests that != (the not equal function) works properly.
        """

        self.assertTrue(ergo("!= 3 9 9 4"))
        self.assertFalse(ergo("!= string string string"))

    def test_len(self):
        """
        Tests that the len function works properly.
        """

        self.assertEqual(ergo("len (list 1 2 3)"), 3)
        self.assertEqual(ergo("len abasd"), 5)

    def test_not(self):
        """
        Tests that the not function works properly.
        """

        self.assertEqual(ergo("not $t"), False)
        self.assertEqual(ergo("not $f"), True)

    def test_float(self):
        """
        Tests that the float function works properly.
        """

        self.assertEqual(ergo("float 1"), 1.0)
        self.assertEqual(ergo("float \"6.37\""), 6.37)

    def test_int(self):
        """
        Tests that the int function works properly.
        """

        self.assertEqual(ergo("int 1.024"), 1)
        self.assertEqual(ergo("int \"123\""), 123)

    def test_str(self):
        """
        Tests that the str function works properly.
        """

        self.assertEqual(ergo("str 1.024"), "1.024")
        self.assertEqual(ergo("str 123"), "123")

    def test_bool(self):
        """
        Tests that the bool function works properly.
        """

        self.assertEqual(ergo("bool 1.024"), True)
        self.assertEqual(ergo("bool 0"), False)
        self.assertEqual(ergo("bool \"abc\""), True)
        self.assertEqual(ergo("bool \"\""), False)

    def test_unique(self):
        """
        Tests that the unique function works properly.
        """

        self.assertEqual(ergo("unique (list 1 2 3)"), [1, 2, 3])
        self.assertEqual(ergo("unique (list 1 2 3 1)"), [1, 2, 3])
        self.assertEqual(ergo("unique (list testing testing testing)"), ['testing'])

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

        self.assertEqual(ergo("print 1 2 3 | first {}"), 1)
        self.assertEqual(ergo("print 4 9 2 | print ${0}"), [4, 9, 2])
        self.assertEqual(ergo("print 2 4 6 8 | print ${1}"), [4, 8])
        self.assertEqual(ergo("print 2 4 6 8 | print ${0/1}"), [2, 6])


    def test_first(self):
        """
        Tests that the first function works properly.
        """

        self.assertEqual(ergo("first (list 4 9 6)"), 4)


    def test_rest(self):
        """
        Tests that the rest function works properly.
        """

        self.assertEqual(set(ergo("rest (list 4 9 6)")), {9, 6})


    def test_last(self):
        """
        Tests that the last function works properly.
        """

        self.assertEqual(ergo("last (list 9 (list 2) 'c')"), "c")

    def test_rrest(self):
        """
        Tests that the rrest function works properly.
        """

        self.assertEqual(ergo("rrest (list 1 2 (list 3 9) 4)"), [1, 2, [3, 9]])

    def test_append(self):
        """
        Tests that the append function works properly.
        """

        self.assertEqual(ergo("append (list 1 2 3) '4'"), [1, 2, 3, '4'])

    def test_list(self):
        """
        Tests that the list function works properly.
        """

        self.assertEqual(set(ergo("list 4 9 a 3 (list 3)"), {4, 9, "a", 3, [3]}))


    def test_split(self):
        """
        Tests that the split function works properly.
        """

        self.assertEqual(set(ergo("split , 1,2,3")), {'1','2','3'})


    def test_flatten(self):
        """
        Tests that the flatten function works properly.
        """

        self.assertEqual(set(ergo("flatten (list (list 1 2 (list 3)) 4 5)")), {1, 2, 3, 4, 5})


    def test_zip(self):
        """
        Tests that the zip function works properly.
        """

        self.assertEqual(set(ergo("zip (list 1 2 3) (list 4 5 6)")), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(ergo("zip abc def")), {"a", "d", "b", "e", "c", "f"})


    def test_apply(self):
        """
        Tests that the apply function works properly.
        """

        self.assertEqual(ergo("apply $= (list 1 2 3)"), False)
        self.assertEqual(ergo("apply $+ (list a b c)"), "abc")

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

        self.assertEqual(ergo("round $pi 2"), 3.14)

    def test_hash(self):
        """
        Tests that the hash function works properly.
        """

        self.assertEqual(ergo("hash (list 1 2 3 '4')"), {1: 2, 3: '4'})

    def test_hash_add(self):
        """
        Tests that the hash function works properly.
        """

        self.assertEqual(ergo("hash-add 9 2 (hash (list 1 2 3 '4'))"), {1: 2, 3: '4', 9: 2})

    def test_hash_rem(self):
        """
        Tests that the hash function works properly.
        """

        self.assertEqual(ergo("hash-rem 1 (hash (list 1 2 3 '4'))"), {3: '4'})

    def test_hash_get(self):
        """
        Tests that the hash function works properly.
        """

        self.assertEqual(ergo("hash-get 3 (hash (list 1 2 3 '4'))"), '4')

    
