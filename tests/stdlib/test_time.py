#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_time.py]

Test the addstring command.
"""

import unittest
from time import strftime, gmtime

from ergonomica.ergo import ergo

STRFTIME_TEST_STRING = "%h'''%m95%daf%Hfd%M52%S"

class TestTime(unittest.TestCase):
    """Tests the 'time' command."""

    def test_time(self):
        """
        Test the time function.
        """

        self.assertEqual(ergo('time {}'.format(STRFTIME_TEST_STRING)), strftime(STRFTIME_TEST_STRING, gmtime()))
