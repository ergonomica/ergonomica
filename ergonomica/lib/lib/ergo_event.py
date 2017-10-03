#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle

def trigger(event, implications):
    for f in implications.get(event, []):
        f()

def event(eventName):

    # load implications store
    implications = pickle.load(open(os.path.expanduser('~/.ergo/.events')))
    
    if isinstance(eventName, list):
        for event in eventName:
            trigger(event, implications)

    elif isinstance(eventName, str):
        trigger(eventName, implications)
