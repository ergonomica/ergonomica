#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_temp.py]

Tests the temp command.
"""

import os
import unittest

from ergonomica.ergo import ergo

class TestTemp(unittest.TestCase):
    """Tests the temp command."""    

    def test_temp(self):
        """
        Tests the temp command.
        """

        # ensure that the filename is not taken
        self.assertFalse(os.path.isfile(ergo("temp file")))

        # ensure that the tempdir was successfully created
        self.assertTrue(os.path.isdir(ergo("temp dir")))
