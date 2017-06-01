"""
[lib/util/setup.py]

The Ergonomica setup script.
"""

import os


def setup():
    """
    Set up the users computer for Ergonomica. Note that this is only
    called when it is known that their computer does not have this structure
    is installed.
    """

    os.mkdir(os.path.join(os.path.expanduser("~"), ".ergo"))
    os.mkdir(os.path.join(os.path.expanduser("~"), ".ergo", "packages"))
    open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile"), "w")
    open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"), "w")
    open(os.path.join(os.path.expanduser("~"), ".ergo", "package", "__init__.py"), "w")
