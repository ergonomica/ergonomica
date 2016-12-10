"""
[lib/lang/runtime.py]

The Ergonomica runtime manager (allows for computing of operations outside of the main Ergonomica
file.
"""

class Runtime(object):
    def __init__(self):
        self.last_args = []
        self.lastlast_args = []
        self.last_kwargs = {}
        self.lastlast_kwargs = {}
        self.verbs = {}
