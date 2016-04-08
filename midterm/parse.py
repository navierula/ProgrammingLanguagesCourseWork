#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# parse.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
#
# Modified by: Navraj Narula


import re

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tmp, top = True):

    tokens = tmp[0:]
    if tokens[0] == [] or tokens[0] == '}':
        return ('End', tokens)
    tokens = tmp[0:]
    result = left(tokens, False)
    if result is not None:
        (e1, tokens) = result
        if tokens == []:
            return result
        elif tokens[0] == '+':
            tokens = tokens[1:]
            result = expression(tokens, False)
            if result is not None:
                (e2, tokens) = result
                if not top or len(tokens) == 0:
                    return ({'Plus':[e1,e2]}, tokens)
        else:
            return result
            

def left(tmp, top = True):

    tokens = tmp[0:]
    if tokens[0] == 'true':
        tokens = tokens[1:]
        if not top or len(tokens) == 0:
            return ('True', tokens)

    tokens = tmp[0:]
    if tokens[0] =='false':
        tokens = tokens[1:]
        if not top or len(tokens) == 0:
            return ('False', tokens)

    tokens = tmp[0:]
    if tokens[0] == '$':
        result = variable(tokens[1:], False)
        if result is not None:
            (e1, tokens) = result
            return (e1, tokens)
            

    tokens = tmp[0:]
    if tokens[0] == '@':
        result = variable(tokens[1:], False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == '[':
                tokens = tokens[1:]
                result = expression(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == ']':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Element':[e1,e2]}, tokens)


    tokens = tmp[0:]
    result = number(tokens, False)
    if result is not None:
        (e1, tokens) = result
        if not top or len(tokens) == 0:
            return (e1, tokens)

def program(tmp, top = True):
    tokens = tmp[0:]
    if tokens[0] == '@':
        result = variable(tokens[1:], False)
        if result is not None:
            (el, tokens) = result
            if tokens[0] == ':=' and tokens[1] == '[':
                tokens = tokens[2:]
                result = expression(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == ',':
                        tokens = tokens[1:]
                        result = expression(tokens, False)
                        if result is not None:
                            (e3, tokens) = result
                            if tokens[0] == ',':
                                tokens = tokens[1:]
                                result = expression(tokens, False)
                                if result is not None:
                                    (e4, tokens) = result
                                    if tokens[0] == ']' and tokens[1] == ';':
                                        tokens = tokens[2:]
                                        result = program(tokens, False)
                                        if result is not None:
                                            (e5, tokens) = result
                                            return ({'Assign':[e1,e2,e3,e4,e5]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'print':
        result = expression(tokens, False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == ';':
                tokens = tokens[1:]
                result = program(tokens, False)
                if result is not None:
                    (e2, tokens) = result
                    return ({'Print':[e1,e2]}, tokens)


    tokens = tmp[0:]
    if tokens[0] == 'loop' and tokens[1] == '$':
        result = variable(tokens[1:], False)
        if result is not None:
            (e1, tokens) = result
            if tokens[0] == 'from':
                tokens = tokens[1:]
                result = number(tokens[1:], False)
                if result is not None:
                    (e2, tokens) = result
                    if tokens[0] == '{':
                        tokens = tokens[1:]
                        result = program(tokens, False)
                        if result is not None:
                            (e3, tokens) = result
                            if tokens[0] == '}':
                                tokens = tokens[1:]
                                result = program(tokens, False)
                                if result is not None:
                                    (e4, tokens) = result
                                    return ({'Loop':[e1,e2,e3,e4]}, tokens)



def tokenizeAndParse(s):
    tokens = re.split(r"(\s+|:=|print|\+|loop|from|{|}|;|\[|\]|,|@|\$)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    pro, tokens = program(tokens)
    return pro



#eof
