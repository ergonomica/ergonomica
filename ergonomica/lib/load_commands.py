#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[load_packages.py]

External package loader.
"""

import os         # for os.path.expanduser()
import sys        # for importing from ~/.ergo/packages
import importlib  # for programatic importing

from ergonomica.lib.lib import ns

packages_path = os.path.join(os.path.expanduser("~"), ".ergo", "packages")

sys.path.append(packages_path)
try:
    for module in os.listdir(packages_path):
        try:
            if module[-3:] != "pyc":
                loaded_module = importlib.import_module(module[:-3])
                ns.update(loaded_module.ns)
        except ImportError:
            pass
except OSError:
    print("[ergo: ConfigError]: No directory ~/.ergo/packages. Please run ergo_setup.")
