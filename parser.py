#
# [parser.py]
#
# Ergonomica's parser.
#

import ply.yacc as yacc

from lexer import tokens

def echo(x):
    print(1)

namespace = {'echo': echo}

def p_definition_definition(p):
    'definition : 

def p_expression_command(p):
    'expression : COMMAND ARGLIST'
    namespace[p[1]](p[1])
    
def p_factor_

def p_function_


def p_error(p):
    print("Syntax error!")

parser = yacc.yacc()

