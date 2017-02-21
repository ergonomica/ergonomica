#!/usr/bin/python
# -*- coding: utf-8 -*-

# this imports verbs for loading by lib/verbs/verbs.py
# pylint: disable=unused-import

# pylint doesn't know where this file is imported from
# pylint: disable=import-error

# "verbs" (lowcase) is standard among all files
# pylint: disable=invalid-name

"""
[load_packages.py]

External package loader.
"""

import os # for os.path.expanduser()
import sys # for importing from ~/.ergo/packages
import importlib # for programatic importing

from lib.lib import verbs

packages_path = os.path.join(os.path.expanduser("~"), ".ergo", "packages")

sys.path.append(packages_path)
try:
    for module in os.listdir(packages_path):
        try:
            if module[-3:] != "pyc":
                loaded_module = importlib.import_module(module[:-3])
                verbs.update(loaded_module.verbs)
        except ImportError:
            pass
except OSError:
    print("[ergo: ConfigError]: No directory ~/.ergo/packages. Please run ergo_setup.")
