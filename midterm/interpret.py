#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
# Modified by: Navraj Narula

exec(open('parse.py').read())

Node = dict
Leaf = str


def evalExpression(env, e):
    
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Plus':
                c1 = children[0]
                c2 = children[1]
                e1 = evalExpression(env, c1)
                e2 = evalExpression(env, c2)
                return e1 + e2
            elif label == 'Number':
                e1 = children[0]
                return e1
            elif label == 'Variable':
                c1 = children[0]
                if c1 in env:
                    e1 = env[c1]
                    return e1
            elif label == 'Element':
                c1 = children[0]
                c2 = children[1]
                var = c1['Variable'][0]
                if var in env:
                    x = evalExpression(env, c2)
                    if x in range(0,3):
                        return x     
    if type(e) == Leaf:
        if e == 'True':
            return 'True'
        if e == 'False':
            return False

def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:        
        for label in s:
            if label == 'Print':
                [e,p] = s[label]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            children = s[label]
            if label == 'Assign':
                var, c1, c2, c3, pro = children
                var = var['Variable'][0]
                e1 = evaluate(env, c1)
                e2 = evaluate(env, c2)
                e3 = evaluate(env, c3)
                env[var] = [e1, e2, e3]
                env, o = execProgram(env, pro)
                return env, o
            if label == 'Loop':
                var = children[0]['Variable'][0]
                num = children[1]['Number'][0]
                pro1 = children[2]
                pro2 = children[3]
                env[var] = num
                if num < 0:
                    # execute p1, update p1
                    (env, o) = execProgram(env, pro2)
                    return (env,o)
                else:
                    env[var] = num #update environment
                    (env, o) = execProgram(env, pro1)
                    children[1]['Number'][0] = num - 1 #changing parse tree
                    (env2, o2) = execProgram(env, s)
                    return (env2, o + o2)


def interpret(s):
    tree = tokenizeAndParse(s)
    (env, o) = execProgram({}, tree)
    return o


#eof
