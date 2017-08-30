#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_sysinfo.py]

Tests the sysinfo command.
"""

import os
import unittest
import platform
import psutil

from ergonomica import ergo

class TestSysinfo(unittest.TestCase):
    """Tests the sysinfo command."""

    def test_sysinfo_stat(self):
        """
        Tests sysinfo on static attributes (sysinfo stat).
        """

        self.assertEqual(ergo("sysinfo stat -apoc"), [", ".join(platform.architecture()),
                                                     platform.processor(),
                                                     platform.platform(),
                                                      str(psutil.cpu_count())])


    def test_sysinfo_dyn(self):
        """
        Tests sysinfo on dynamic attributes (sysinfo dyn).
        """

        # cpu percent usage will likely change by the time second operation is done.
        # this simply tests that `sysinfo dyn -p` won't throw an error

        ergo("sysinfo dyn -u")

