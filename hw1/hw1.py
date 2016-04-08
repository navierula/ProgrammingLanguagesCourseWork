# Name: Navraj (Navie) Narula
# CS320: Grammars, Lexing, and Parsing
# HW1
# September 16, 2015

# I collaborated with Shahrez Jan, John Gonsalves, and Phong Pham.

import re

def regexp(tokens):

    res = "("
    for i in range(len(tokens)):
        if tokens[i] == '$' or tokens[i] =="?" or tokens[i] == '*' or tokens[i] == '+' or tokens[i] == '(' or tokens[i] == ')' or tokens[i] == '#':
            res = res + "\\"
        res = res + tokens[i]
        if i < len(tokens)-1:
            res = res + "|"
    res = res + ")"
    return res

def tokenize(terminals, string):
    
    terminals = [t for t in re.split(regexp(terminals), string)]        
    return [t for t in terminals if not t.isspace() and not t == ""]


def tree(tokens):
    if tokens[0] == 'two' and tokens[1] == 'children' and tokens[2] == 'start':
        (e1, tokens) = tree(tokens[3:])
        if tokens[0] == ';':
            (e2, tokens) = tree(tokens[1:])
            if tokens[0] == 'end':
              return ({'Two':[e1,e2]}, tokens[1:])

    if tokens[0] == 'one' and tokens[1] == 'child' and tokens[2] == 'start':
        (e1, tokens) = tree(tokens[3:])
        if tokens[0] == 'end':
          return ({'One': [e1]}, tokens[1:])

    if tokens[0] == 'zero' and tokens[1] == 'children':
        return ('Zero', tokens[2:])

def number(tokens):
    if re.match(r"^(0|[0-9]+)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens):
    if re.match(r"^[a-z]|[A-Z]*", tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

def term(tmp, top = True):
    tokens = tmp[0:]
    if tokens[0] == 'plus' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        return ({'Plus':[e1,e2]}, tokens) 

    tokens = tmp[0:]
    if tokens[0] == 'max' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        return ({'Max':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == 'max':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        return ({'Max':[e1,e2]}, tokens)
    
    tokens = tmp[0:]
    if tokens[0] == 'if' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ',':
                        tokens = tokens[1:]
                        r = term(tokens, False)
                        if not r is None:
                            (e3, tokens) = r
                            if tokens[0] == ')':
                                tokens = tokens[1:]
                                return ({'If':[e1,e2,e3]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '?':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ':':
                        tokens = tokens[1:]
                        r = term(tokens, False)
                        if not r is None:
                            (e3, tokens) = r
                            if tokens[0] == ')':
                                tokens = tokens[1:]
                                return ({'If':[e1,e2,e3]}, tokens)
                                    
    tokens = tmp[0:]
    if tokens[0] == '#':
        tokens = tokens[1:]
        return (number(tokens))
    
    tokens = tmp[0:]
    if tokens[0] == '$':
        tokens = tokens[1:]
        return (variable(tokens))

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '+':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        return ({'Plus':[e1,e2]}, tokens)

                            
def formula(tmp, top = True):  

    tokens = tmp[0:]
    if tokens[0] == 'true':
        tokens = tokens[1:]
        if not top or len(tokens) == 0:
            return ('True', tokens)

    tokens = tmp[0:]
    if tokens[0] == 'false':
        tokens = tokens[1:]
        if not top or len(tokens) == 0: 
            return ('False', tokens)

    tokens = tmp[0:]
    if tokens[0] == 'not' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ')':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'Not':[e1]}, tokens)

    tokens = tmp[0:]  
    if tokens[0] == 'xor' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = formula(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                             return ({'Xor':[e1,e2]}, tokens)
    
    tokens = tmp[0:]
    if tokens[0] == 'equal' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                             return ({'Equal':[e1,e2]}, tokens)   

    tokens = tmp[0:]
    if tokens[0] == 'less' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                             return ({'Less':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'greater' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                             return ({'Greater':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '<':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Less':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '>':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Greater':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == 'xor':
                tokens = tokens[1:]
                r = formula(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Xor':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '=' and tokens[1] == '=' :
                tokens = tokens[2:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Equal':[e1,e2]}, tokens)

def program(tmp, top = True):
    
    tokens = tmp[0:]
    if tokens[0] == 'print':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ';':
                tokens = tokens[1:]
                r = program(tokens, False)
                if not r is None:
                    if type(r) == type(""):
                        e2 = r
                        tokens = []
                    else:
                        (e2, tokens) = r
                    return ({'Print':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'input' and tokens[1] == '$':
        tokens = tokens[2:]
        r = variable(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ';':
                tokens = tokens[1:]
                r = program(tokens, False)
                if not r is None:
                    if type(r) == type(""):
                        e2 = r
                        tokens = []
                    else:
                        (e2, tokens) = r
                    return ({'Input':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'assign' and tokens[1] == '$':
        tokens = tokens[2:]
        r = variable(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ':' and tokens[1] == '=':
                tokens = tokens[2:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ';':
                        tokens = tokens[1:]
                        r = program(tokens, False)
                        if not r is None:
                            if type(r) == type(""):
                                e3 = r
                                tokens = []
                            else:
                                (e3, tokens) = r
                            return ({'Assign':[e1,e2,e3]}, tokens)
               
    tokens = tmp[0:]
    if tokens[0] == 'end' and tokens[1] == ';':
        return ('End')

def parse(string):
    
    token_list = ["plus", "max", "if", "variable", "number", "true", "false", "not",
    "xor", "equal", "less", "greater", "print", "input",
    "assign", "end", "\#", "\$", "\?", "\=", "\+", "\(", "\)", "\*", ",", ";", ":", "\<", "\>",
    '[0-9]+','-[0-9]+', '[a-zA-Z]+']
    
    tokens = tokenize(token_list, string)

    if re.match(r"^plus|max|if|variable|number", tokens[0]):
        return term(tokens)

    if re.match(r"^true|false|not|xor|equal|less|greater", tokens[0]):
        return formula(tokens)
    
    if re.match(r"^print|input|assign|end", tokens[0]):
        p = program(tokens)
        if p == "End":
            return p
        if p == None:
            return None
        return p[0]



































    
    
