#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

try:
    input = raw_input
    range = xrange
except:
    pass


import re
import sys
import io
import collections


class Symbol(str):
    pass


def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]

_quote, _if, _set, _define, _lambda, _begin, _definemacro, = list(map(Sym,
"quote   if   set!  define   lambda   begin   define-macro".split()))

_quasiquote, _unquote, _unquotesplicing = list(map(Sym,
"quasiquote   unquote   unquote-splicing".split()))


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, parms, exp, namespace):
        self.parms, self.exp, self.namespace = parms, exp, namespace

    def __call__(self, *args):
        return eval(self.exp, Namespace(self.parms, args, self.namespace))


################ parse, read, and user interaction
def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an InPort
    if isinstance(inport, str):
        inport = InPort(io.StringIO(inport))
    return expand(read(inport), toplevel=True)

eof_object = Symbol('#<eof-object>')    # Note: uninterned; can't be read


class InPort(object):
    "An input port. Retains a line of chars."
    tokenizer = (
        r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)""")

    def __init__(self, file):
        self.file, self.line = file, ''

    def next_token(self):
        "Return the next token, reading new text into line buffer if needed."
        while True:
            if self.line == '':
                self.line = self.file.readline()
            if self.line == '':
                return eof_object
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token


def readchar(inport):
    "Read the next character from an input port."
    if inport.line != '':
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or eof_object


def read(inport):
    "Read a Scheme expression from an input port."
    def read_ahead(token):
        if '(' == token:
            L = []
            while True:
                token = inport.next_token()
                if token == ')':
                    return L
                else:
                    L.append(read_ahead(token))
        elif ')' == token:
            raise SyntaxError('unexpected )')
        elif token in quotes:
            return [quotes[token], read(inport)]
        elif token is eof_object:
            raise SyntaxError('unexpected EOF in list')
        else:
            return atom(token)
    # body of read:
    token1 = inport.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)

quotes = {"'": _quote, "`": _quasiquote, ",": _unquote, ",@": _unquotesplicing}


def atom(token):
    '''Numbers become numbers; #t and #f are booleans;
        "..." string; otherwise Symbol.

    '''

    if token == '#t':
        return True
    elif token == '#f':
        return False
    elif token[0] == '"':
        try:
            return bytes(token[1:-1], "utf-8").decode("unicode_escape")
        except TypeError:
            # Python 2
            return token[1:-1].decode('string_escape')

    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Sym(token)


def to_string(x):
    "Convert a Python object back into a Lisp-readable string."
    if x is True:
        return "#t"
    elif x is False:
        return "#f"
    elif isa(x, Symbol):
        return x
    elif isa(x, str):
        try:
            return '"%s"' % bytes(x, "utf-8").decode("unicode_escape").replace('"', r'\"')
        except TypeError:
            # Python 2
            return '"%s"' % x.encode('string_escape').replace('"',r'\"')

    elif isa(x, list):
        return '(' + ' '.join(map(to_string, x)) + ')'
    elif isa(x, complex):
        return str(x).replace('j', 'i')
    else:
        return str(x)


def load(filename):
    "Eval every expression from a file."
    repl(None, InPort(open(filename)), None)


def repl(prompt='lispy> ', inport=InPort(sys.stdin), out=sys.stdout):
    "A prompt-read-eval-print loop."
    sys.stderr.write("Lispy version 2.0\n")
    while True:
        try:
            if prompt:
                sys.stderr.write(prompt)
                sys.stderr.flush()
            x = parse(inport)
            if x is eof_object:
                return
            val = eval(x)
            if val is not None and out:
                print(to_string(val), file=out)
        except Exception as e:
            print('%s: %s' % (type(e).__name__, e))


################ Environment class
class Namespace(dict):
    "An namespace: a dict of {'var':val} pairs, with an outer Namespace."

    def __init__(self, parms=(), args=(), outer=None):
        # Bind parm list to corresponding args, or single parm to list of args
        self.outer = outer
        if isa(parms, Symbol):
            self.update({parms: list(args)})
        else:
            if len(args) != len(parms):
                raise TypeError('expected %s, given %s, '
                                % (to_string(parms), to_string(args)))
            self.update(list(zip(parms, args)))

    def find(self, var):
        "Find the innermost Namespace where var appears."
        if var in self:
            return self
        elif self.outer is None:
            raise LookupError(var)
        else:
            return self.outer.find(var)


def is_pair(x):
    return x != [] and isa(x, list)


def cons(x, y):
    return [x] + y


def callcc(proc):
    "Call proc with current continuation; escape only"
    ball = RuntimeWarning(
            "Sorry, can't continue this continuation any longer.")

    def throw(retval):
        ball.retval = retval
        raise ball

    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball:
            return ball.retval
        else:
            raise w


def add_globals(self):
    "Add some Scheme standard procedures."
    import math
    import cmath
    import operator as op

    self.update(vars(math))
    self.update(vars(cmath))
    self.update({
     'print': lambda x: x, '+': lambda *x: sum(x), '-': op.sub, '*': op.mul, '/': op.truediv, 'not': op.not_,
     '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
     'equal?': op.eq, 'eq?': op.is_, 'length': len, 'cons': cons,
     'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'append': op.add,
     'list': lambda *x: list(x), 'list?':  lambda x: isa(x, list),
     'null?': lambda x: x == [], 'symbol?': lambda x: isa(x, Symbol),
     'boolean?': lambda x: isa(x, bool), 'pair?': is_pair,
     'port?':  lambda x: isa(x, file), 'apply': lambda proc, l: proc(*l),
     'eval': lambda x: eval(expand(x)), 'load': lambda fn: load(fn),
     'call/cc': callcc,
      'open-input-file': open, 'close-input-port': lambda p: p.file.close(),
     'open-output-file': lambda f: open(f, 'w'),
     'close-output-port': lambda p: p.close(),
     'eof-object?': lambda x: x is eof_object, 'read-char': readchar,
     'read': read, 'write':
                    lambda x, port=sys.stdout: port.write(to_string(x)),
     'display': lambda x, port=sys.stdout: port.write(x
                                                    if isa(x, str)
                                                    else to_string(x))})
    return self

isa = isinstance

global_namespace = add_globals(Namespace())


################ eval (tail recursive)
def eval(x, namespace=global_namespace):
    "Evaluate an expression in an namespace."
    while True:
        if isa(x, Symbol):       # variable reference
            return namespace.find(x)[x]
        elif not isa(x, list):   # constant literal
            return x
        elif x[0] is _quote:     # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] is _if:        # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if eval(test, namespace) else alt)
        elif x[0] is _set:       # (set! var exp)
            (_, var, exp) = x
            namespace.find(var)[var] = eval(exp, namespace)
            return None
        elif x[0] is _define:    # (define var exp)
            (_, var, exp) = x
            namespace[var] = eval(exp, namespace)
            return None
        elif x[0] is _lambda:    # (lambda (var*) exp)
            (_, vars, exp) = x
            return Procedure(vars, exp, namespace)
        elif x[0] is _begin:     # (begin exp+)
            for exp in x[1:-1]:
                eval(exp, namespace)
            x = x[-1]
        else:                    # (proc exp*)
            exps = [eval(exp, namespace) for exp in x]
            proc = exps.pop(0)
            if isa(proc, Procedure):
                x = proc.exp
                namespace = Namespace(proc.parms, exps, proc.namespace)
            else:
                return proc(*exps)


def require(x, predicate, msg="wrong length"):
    "Signal a syntax error if predicate is false."
    if not predicate:
        raise SyntaxError(to_string(x) + ': ' + msg)


################ expand
def expand(x, toplevel=False):
    "Walk tree of x, making optimizations/fixes, and signaling SyntaxError."
    require(x, x != [])                 # () => Error
    if not isa(x, list):                # constant => unchanged
        return x
    elif x[0] is _quote:                # (quote exp)
        require(x, len(x) == 2)
        return x
    elif x[0] is _if:
        if len(x) == 3:
            x = x + [None]              # (if t c) => (if t c None)
        require(x, len(x) == 4)
        return list(list(map(expand, x)))
    elif x[0] is _set:
        require(x, len(x) == 3)
        var = x[1]                      # (set! non-var exp) => Error
        require(x, isa(var, Symbol), "can set! only a symbol")
        return [_set, var, expand(x[2])]
    elif x[0] is _define or x[0] is _definemacro:
        require(x, len(x) >= 3)
        _def, v, body = x[0], x[1], x[2:]
        if isa(v, list) and v:          # (define (f args) body)
            f, args = v[0], v[1:]       # => (define f (lambda (args) body))
            return expand([_def, f, [_lambda, args] + body])
        else:
            require(x, len(x) == 3)       # (define non-var/list exp) => Error
            require(x, isa(v, Symbol), "can define only a symbol")
            exp = expand(x[2])
            if _def is _definemacro:
                require(x, toplevel, "define-macro only allowed at top level")
                proc = eval(exp)
                require(x, isinstance(proc, collections.Callable),
                                        "macro must be a procedure")
                macro_table[v] = proc   # (define-macro v proc)
                return None             # => None; add v:proc to macro_table
            return [_define, v, exp]
    elif x[0] is _begin:
        if len(x) == 1:
            return None                 # (begin) => None
        else:
            return [expand(xi, toplevel) for xi in x]
    elif x[0] is _lambda:               # (lambda (x) e1 e2)
        require(x, len(x) >= 3)           # => (lambda (x) (begin e1 e2))
        vars, body = x[1], x[2:]
        require(x, (isa(vars, list) and all(isa(v, Symbol) for v in vars))
                or isa(vars, Symbol), "illegal lambda argument list")
        exp = body[0] if len(body) == 1 else [_begin] + body
        return [_lambda, vars, expand(exp)]
    elif x[0] is _quasiquote:           # `x => expand_quasiquote(x)
        require(x, len(x) == 2)
        return expand_quasiquote(x[1])
    elif isa(x[0], Symbol) and x[0] in macro_table:
        return expand(macro_table[x[0]](*x[1:]), toplevel)  # (m arg...)
    else:                                # => macroexpand if m isa macro
        return list(list(map(expand, x)))   # (f arg...) => expand each

_append, _cons, _let = list(map(Sym, "append cons let".split()))


def expand_quasiquote(x):
    """Expand `x => 'x; `,x => x; `(,@x y) => (append x y) """
    if not is_pair(x):
        return [_quote, x]
    require(x, x[0] is not _unquotesplicing, "can't splice here")
    if x[0] is _unquote:
        require(x, len(x) == 2)
        return x[1]
    elif is_pair(x[0]) and x[0][0] is _unquotesplicing:
        require(x[0], len(x[0]) == 2)
        return [_append, x[0][1], expand_quasiquote(x[1:])]
    else:
        return [_cons, expand_quasiquote(x[0]), expand_quasiquote(x[1:])]


def let(*args):
    args = list(args)
    x = cons(_let, args)
    require(x, len(args) > 1)
    bindings, body = args[0], args[1:]
    require(x, all(isa(b, list) and len(b) == 2 and isa(b[0], Symbol)
                   for b in bindings), "illegal binding list")
    vars, vals = list(zip(*bindings))
    return ([[_lambda, list(vars)] + list(map(expand, body))]
            + list(map(expand, vals)))

macro_table = {_let: let}   # More macros can go here

#eval(parse(u"""(begin
#
#(define-macro and (lambda args
#   (if (null? args) #t
#       (if (= (length args) 1) (car args)
#           `(if ,(car args) (and ,@(cdr args)) #f)))))
#
#;; More macros can also go here
#
#)"""))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        repl()
    else:
        load(sys.argv[1])
