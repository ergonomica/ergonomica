#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_cd.py]

Test the cd command.
"""

import unittest
import os
import tempfile

from ergonomica import ergo

class TestCd(unittest.TestCase):
    """Tests the cd command."""

    def test_cd(self):
        """
        Tests the cd command.
        """

        olddir = os.getcwd()
        newdir = tempfile.mkdtemp()

        ergo("cd {}".format(newdir))

        self.assertEqual(os.getcwd(), newdir)

        ergo("cd {}".format(olddir))

        self.assertEqual(os.getcwd(), olddir)


