#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lib/tree.py]

Defines the "tree" command.
"""

import os
import datetime
from ergonomica.lib.util.util import expand_path

def build_tree(directory):
        
    items = [os.path.join(directory, x) for x in os.listdir(directory)]
        
    files = [x for x in items if os.path.isfile(x)]
    directories = [x for x in items if os.path.isdir(x)]
    
    tree = {directory: files}
    
    for x in directories:
        tree[directory].append(build_tree(x))

    return tree

def print_tree(tree):
    out = []
    
    if isinstance(tree, str):
        # aka we've reached a file
        return tree
    elif isinstance(tree, list):
        return tree
    
    # parent dir
    parent = tree.keys()[0]
    
    # print the head
    out.append('├─ ' + os.path.basename(parent))
    
    # recurse
    for i in tree[parent]:
        
        if isinstance(i, str):
            # a leaf
            out.append('├─ ' + os.path.basename(i))
            
        if isinstance(i, dict):
            # a directory
            #out.append('├─' + i)
            subtree = print_tree(i)
            out += [subtree[0]] + ['│    ' + x for x in subtree[1:]]

    return out

def tree(argc):
    """
    tree: Show the directory tree.

    Usage:
        tree [DIR]
    """
    
    # first build the tree
    directory = expand_path(argc.env, (argc.args['DIR'] if argc.args['DIR'] else '.'))
    tree = build_tree(directory)

    return print_tree(tree)

exports = {'tree': tree}


