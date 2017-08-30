#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_list_modules.py]

Test the list_modules command.
"""

import os
import unittest

from ergonomica import ergo

class TestListModules(unittest.TestCase):
    """Tests the list_modules command."""

    # TODO: complete this
    def test_list_modules(self):
        """
        Tests the list_modules command.
        """

        # old (confirmed working) implementation. test that any new implementation will match.
        files = os.listdir(os.path.join(os.path.join(os.path.expanduser("~"), ".ergo"), "packages"))
        self.assertEqual(ergo('list_modules'), [f.replace(".py", "") for f in files if f.endswith(".py") and f != "__init__.py"])


