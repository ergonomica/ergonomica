#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/arguments.py]

"""

def get_args_kwargs(env, tokenized_block, pipe):
    args = tokenized_block[0][1:]
    kwargs = {s.split(":")[0]:eval(s.split(":")[1], env.namespace) for s in tokenized_block[1]}
    try:
        if tokenized_block[0][1:][0].startswith("--"):
            selectors = tokenized_block[0][1:][0].split(",")
            if "--arg" in selectors:
                args = pipe.getstack_args(-1) + args[1:]
            elif "--kw" in selectors:
                kwargs.update(pipe.getstack_kwargs(-1))
    except IndexError:
        pass
    return args, kwargs

def get_func(tokenized_block, verbs):
    try:
        func = verbs[tokenized_block[0][0]]
    except KeyError:
        if len(tokenized_block[0][0]) == 3:
            try:
                func = verbs[[x for x in verbs if tokenized_block[0][0] == x[:3]][0]]
            except IndexError:
                raise KeyError
        else:
            raise KeyError
    return func
