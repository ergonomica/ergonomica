#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/schedule.py]

Defines the "schedule" command.
"""

import schedule as schedule_module

verbs = {}

def raw_schedule(r, l, f):
    if l == []:
        r.do(f)
    else:
        raw_schedule(getattr(r, l[0]), l[1:], f)

def ergo_schedule(argc):
    """
    schedule: Single-process, Python alternative to Cron.
    
    Usage:
       schedule FUNCTION every ARGS...
    """

    raw_schedule(schedule_module.every(), argc.args['ARGS'], argc.args['FUNCTION'])
