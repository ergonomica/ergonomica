#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import dill

def trigger(event, implications):
    for f in implications.get(event, []):
        f()

def event(events):

    try:
        # load implications store
        implications = dill.load(open(os.path.expanduser('~/.ergo/.events')))
    except IOError:
        implications = {}

    if not isinstance(events, list):
        events = [events]
    
    for event in events:
        trigger(event, implications)

exports = {'event': event}
