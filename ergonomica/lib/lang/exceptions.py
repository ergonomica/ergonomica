#!/usr/bin/python
# -*- coding: utf-8 -*-

class ErgonomicaException(Exception):
    def __init__(self):
        Exception.__init__(self)
    
class ErgonomicaNameError(ErgonomicaException):
