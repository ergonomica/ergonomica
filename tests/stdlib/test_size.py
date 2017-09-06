#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_size.py]

Tests the size command.
"""

import os
import unittest
import random

from ergonomica import ergo

def file_or_dir_size(path):
    """Return the size of a file or directory."""
    if (os.path.isdir(path)):
        for root, dirs, files in os.walk(path):
            names = files + dirs
            return sum(file_or_dir_size(os.path.join(root, name)) for name in names)
    elif os.path.isfile(path):
        return os.path.getsize(path)
    # Dangling symlinks gets here
    return 0

class TestSize(unittest.TestCase):
    """Tests the size command."""

    def test_size(self):
        """
        Tests the size command.
        """

        # create a file of a random size
        randsize = random.randint(1, 100000)

        # create the file
        with open("test_size", "wb") as f:
            f.seek(randsize)
            f.write(b"testing")

        # ensure the size is correct in bytes and kilobytes
        self.assertEqual(ergo("size -uh byte test_size"), "test_size: " +
                         str(float(file_or_dir_size("test_size"))) + " byte(s)")

        self.assertEqual(ergo("size -uhh B test_size"), "test_size: " +
                         str(float(file_or_dir_size("test_size"))) + " byte(s)")

        self.assertEqual(ergo("size -h test_size"), "test_size: " +
                         str(file_or_dir_size("test_size") / 1024.0) + " kilobyte(s)")

        os.remove("test_size")

