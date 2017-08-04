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

        with open("test-download") as f:
            self.assertEqual(f.read(), "this\nis\na\ntest!\n")

        os.remove("test-download")
