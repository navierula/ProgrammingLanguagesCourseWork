import re

#Name: Navraj Narula
#CS320 HW2: Parsing Algorithms and Interpreters
#Oct. 2, 2015


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

def number(tokens, top = True):
    if re.match(r"^(0|[1-9]|[0-9]*)$", tokens[0]):
        return ((int(tokens[0]), tokens[1:]))

def variable(tokens, top = True):
    string = tokens[0]
    if re.match(r"[a-z]$",string[0]):
        return (string, tokens[1:])


def formula(tmp, top = True):
    
    tokens = tmp[0:]
    result = leftFormula(tokens, False)
    if result is not None:
       (e1, tokens) = result
       if tokens == []:
           return result
       elif tokens[0]== 'and':
           tokens = tokens[1:]
           result = formula(tokens, False)
           if result is not None:
               (e2, tokens) = result
               if not top or len(tokens) == 0:
                   return ({'And':[e1,e2]}, tokens) 
       else:
           return result

def leftFormula(tmp, top = True):

    tokens = tmp[0:] 
    if tokens[0] == 'not' and tokens[1] == '(':
        tokens = tokens[2:]
        result = formula(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ')':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'Not':[e1]}, tokens)
                
    tokens = tmp[0:]
    if tokens[0] == 'nonzero' and tokens[1] == '(':
        tokens = tokens[2:]
        result = term(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ')':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'Nonzero':[e1]}, tokens)

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
    if re.match(r"^(and|nonzero|not|true|false)$", tokens[0]):
        return None
    result = variable(tokens, False)
    if result is not None:
        (e1, tokens) = result
        return ({'Variable':[e1]}, tokens)

def term(tmp, top = True):
    
    tokens = tmp[0:]
    result = factor(tokens, False)
    if result is not None:
        (e1, tokens) = result
        if tokens == []:
            return result
        elif tokens[0] == '+':
            tokens = tokens[1:]
            result = term(tokens,False)
            if result is not None:
                (e2, tokens) = result
                if not top or len(tokens) == 0:
                    return ({'Plus':[e1,e2]}, tokens)
        else:
            return result

def factor(tmp, top = True):
    
    tokens = tmp[0:]
    result = leftFactor(tokens, False)
    if result is not None:
        (e1, tokens) = result
        if tokens == []:
            return result
        elif tokens[0] == '*':
            result = factor(tokens[1:], False)
            if result is not None:
                (e2, tokens) = result
                if not top or len(tokens) == 0:
                    return ({'Mult':[e1,e2]}, tokens)

        else:
            return result

def leftFactor(tmp, top = True):

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        result = term(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ')':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'Parens':[e1]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'if' and tokens[1] == '(':
        tokens = tokens[2:]
        result = formula(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ',':
                tokens = tokens[1:]
                result = term(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == ',':
                        tokens = tokens[1:]
                        result = term(tokens, False)
                        if result is not None:
                            (e3, tokens) = result
                            if tokens[0] == ')':
                                tokens = tokens[1:]
                                if not top or len(tokens) == 0:
                                    return ({'If':[e1,e2,e3]}, tokens)

    tokens = tmp[0:]      
    result = number(tokens, False)
    if result is not None:
        (e1, tokens) = result
        if not top or len(tokens) == 0:
            return ({'Number':[e1]}, tokens)

    tokens = tmp[0:]
    result = variable(tokens, False)
    if re.match(r"^(and|nonzero|not|true|false)$", tokens[0]):
        return None
    result = variable(tokens, False)
    if result is not None:
        (e1, tokens) = result
        if not top or len(tokens) == 0:
            return ({'Variable':[e1]}, tokens)

    
def program(tmp, top = True):

    tokens = tmp[0:]
    if tokens == [] or tokens[0] == "}":
        return ('End', tokens)


    tokens = tmp[0:]
    if tokens[0] == 'print':
        tokens = tokens[1:]
        result = expression(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ';':
                tokens = tokens[1:]
                result = program(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if not top or len(tokens) == 0:
                        return ({'Print':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'assign':
        tokens = tokens[1:]
        result = variable(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ':=':
                tokens = tokens[1:]
                result = expression(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == ';':
                        tokens = tokens[1:]
                        result = program(tokens, False)
                        if result is not None:
                            (e3, tokens) = result
                            if not top or len(tokens) == 0:
                                return ({'Assign':[{'Variable':[e1]},e2,e3]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'if':
        tokens = tokens[1:]
        result = expression(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == '{':
                tokens = tokens[1:]
                result = program(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == '}':
                        tokens = tokens[1:]
                        result = program(tokens, False)
                        if result is not None:
                            (e3, tokens) = result
                            if not top or len(tokens) == 0:
                                return ({'If':[e1,e2,e3]}, tokens)


    tokens = tmp[0:]
    if tokens[0] == 'do' and tokens[1] == '{':
        tokens = tokens[2:]
        result = program(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == '}' and tokens[1] == 'until':
                tokens = tokens[2:]
                result = expression(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == ';':
                        tokens = tokens[1:]
                        result = program(tokens, False)
                        if result is not None:
                            (e3, tokens) = result
                            if not top or len(tokens) == 0:
                                return ({'DoUntil':[e1,e2,e3]}, tokens)
                       

def expression(tmp, top = True):
    
    tokens = tmp[0:]
    form = formula(tokens, False)
    ter = term(tokens, False)
    if form is None:
        return ter
    elif ter is None:
        return form
    elif len(form[1]) > len(ter[1]):
        return ter
    elif len(form[1]) == len(ter[1]):
        return ter
    elif len(form[1]) < len(ter[1]):
        return form
    else:
        return None


