#!/usr/bin/env python
from lark import Lark, Transformer

rules=r'''
?start: obj*
?obj: TEXT -> text
    | tag

tag: "[" key meta obj* "]"

meta: "{" [pair ("," pair)*] "}"
pair: key ":" string

key: KEY
string: ESCAPED_STRING

KEY: /[A-z0-9-_]+/
TEXT: /(\\.|[^\\{}\[\]])+/s
ESCAPED_STRING: /"(\\.|[^"\\])*"/

%import common.WS
%ignore WS
'''

l = Lark(rules, parser='lalr', start="start")

class Tag:
    def __init__(self, key, meta, vals):
        self.vals = vals
        self.key = key
        self.meta = meta

class ToAst(Transformer):
    start = lambda _,x: x if len(x) else None
    tag = lambda _,x: Tag(x[0], x[1], x[2])
    key = lambda _,x: x[0].value
    string = lambda _,x: x[0].value
    meta = lambda _,x: { d[0]: d[1] for d in x } 
    pair = lambda _,x: [x[0], x[1]]
    text = lambda _,x: x[0].value

def parse(data):
    tree = l.parse(data)
    a = ToAst().transform(tree)
    objs = [e for e in a if not isinstance(e, str)]
    return ["".join(map(lambda e: e if isinstance(e, str) else e.vals, a)), objs]

