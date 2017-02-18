#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

Lexer module. Contains tokenize().
"""

# why is this a thing?
# pylint: disable=too-few-public-methods
# pylint: disable=super-init-not-called

import re
from ast import literal_eval

class Pipeline(object):
    """An Ergonomica pipeline object."""
    def __init__(self):
        """Initialize a pipeline."""
        pass
    
class StaticPipeline(Pipeline):
    """A static pipeline (synchronous)."""
    def __init__(self):
        """Initialize a StaticPipeline."""
        self.args = [None, None]
        self.kwargs = [None, None]
    def getstack_args(self,index=-1):
        """Get args from pipeline. Defaults to last value."""
        try:
            return self.args[index]
        except IndexError:
            return None

    def getstack_kwargs(self,index=-1):
        """Get kwargs from pipeline. Defaults to last value."""
        try:
            return self.kwargs[index]
        except IndexError:
            return None
        
    def setstack_args(self,item):
        """Add args to pipeline."""
        self.args.append(item)
        
    def setstack_kwargs(self, item):
        """Remove args from pipeline."""
        self.kwargs.append(item)

    def prune(self):
        """Remove None objects from pipeline."""
        i = 0

        # ansi escape regexp
        ansi_escape = re.compile(r'\x1b[^m]*m')
        
        while i < len(self.args):
            while i < len(self.args) and self.args[i] is None:
                del self.args[i]
            if self.args != [] and i <= len(self.args) and isinstance(self.args[i], list):
                self.args[i] = [ansi_escape.sub('', x) for x in self.args[i]]
            i += 1
            
        self.kwargs = [literal_eval("'%s'" % x) for x in self.kwargs if x is not None]

#class DynamicPipeline(Pipeline):
