#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle

def trigger(event, implications):
    for f in implications.get(event, []):
        f()

def event(events):
    
    # load implications store
    implications = pickle.load(open(os.path.expanduser('~/.ergo/.events')))

    if not isinstance(events, list):
        events = [events]
    
    for event in events:
        trigger(event, implications)
