#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_download.py]

Tests the download command.
"""

import os
import unittest

from ergonomica.ergo import ergo

class TestDownload(unittest.TestCase):
    """Tests the download command."""

    def test_download(self):
        """
        Tests the download command.
        """

        ergo("download http://ergonomica.github.io/test-download")

        self.assertEqual(open("test-download").read(),
                         "this\nis\na\test!\n")

        os.remove("test-download")
