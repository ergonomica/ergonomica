#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ErgonomicaError(Exception):
    pass

def ergo(*argc, **argv):
    from ergonomica.lib.lang.interpreter import ergo as _ergo
    return _ergo(*argc, **argv)

def ergo_to_string(*argc, **argv):
    from ergonomica.lib.lang.interpreter import ergo_to_string
    return ergo_to_string(*argc, **argv)


