#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lang/precompiler.py]

Compiles Ergonomica to raw ErgoLisp.
"""

#from ergononomica.ergo import parse

# print 1 5 3 9
#
# define f
#    print 1 45 14 154 1412
#

def leading_whitespace(string):
    """
    Return the number of leading indents on a line.
    """
    
    for i in range(len(string))[::-1]:
        if string.startswith(" " * i):
            return i
    return 0
        

def precompile(string):
    processed_lines = []
    lines = string.split("\n")
    for i in enumerate(lines):
        if i[0] == 0:
            last_indent = 0
        else:
            last_indent = leading_whitespace(lines[i[0] - 1])

        current_indent = leading_whitespace(i[1])
        
        if i[1].strip() != "":
            processed_lines.append("(" + i[1].strip() + ")")
                
        if current_indent > last_indent:
            processed_lines[-2] = processed_lines[-2][:-1]
            #processed_lines[-2] = processed_lines[-2][:-1]
            
        elif current_indent < last_indent:
            processed_lines[-1] += ")" * ((last_indent - current_indent) / 3)
        
    return " ".join(processed_lines)


print(precompile(
"""define (factorial n acc)
   if (= n 0) acc
      factorial (- n 1) (* n acc)
"""))