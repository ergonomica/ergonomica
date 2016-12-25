#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

Lexer module. Contains tokenize().
"""

# why is this a thing?
# pylint: disable=too-few-public-methods
# pylint: disable=super-init-not-called

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
        self.args = [x for x in self.args if x is not None]                                                                                                                                  
        self.kwargs = [x for x in self.kwargs if x is not None]

#class DynamicPipeline(Pipeline):
