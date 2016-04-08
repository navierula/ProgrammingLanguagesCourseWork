exec(open('parse.py').read())

Node = dict
Leaf = str

# Navraj Narula
# Homework 3 - interpret.py
# CS320

def vnot(v):
    if v == 'True':  return 'False'
    if v == 'False': return 'True'

def vand(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True':  return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'

def vor(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'True'
    if v1 == 'False' and v2 == 'True':  return 'True'
    if v1 == 'False' and v2 == 'False': return 'False'

def xor(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'False'
    if v1 == 'True'  and v2 == 'False': return 'True'
    if v1 == 'False' and v2 == 'True':  return 'True'
    if v1 == 'False' and v2 == 'False': return 'False'
    

def evaluate(env, e):
    if not evalTerm(env,e) == None:
        return evalTerm(env,e)
    else:
        return evalFormula(env,e)

def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':               
                x = children[0]
                return {'Number': [x]}
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                return {'Number':[v1['Number'][0] + v2['Number'][0]]}

def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()                   
            elif label == 'Nonzero':
                t = children[0]
                v = evalTerm(env, t)
            elif label == 'Not':
                f = children[0]
                v = evalFormula(env, f)
                return vnot(v)
            elif label == 'And':
                f1 = children[0]
                f2 = children[1]
                v1 = evalFormula(env, f1)
                v2 = evalFormula(env, f2)
                return vand(v1,v2)
            elif label == 'Xor':
                f1 = children[0]
                f2 = children[1]
                v1 = evalFormula(env, f1)
                v2 = evalFormula(env, f2)
                return xor(v1,v2)
    elif type(f) == Leaf:
        if f == 'True':
            return 'True' 
        if f == 'False':
            return 'False' 
    else:
        return None
    

def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                p = children[1]
                e = children[0]
                v = evaluate(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            if label == 'Assign':
                children = s[label]
                v = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                x = evaluate(env,e)
                env[v] = x
                return execProgram(env,p)               
            elif label == 'If':
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evaluate(env1, e) == 'True':
                    (env2, o1) = execProgram(env1,p1)
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)
                else:
                    (env2, o1) = execProgram(env1, p2)
                    return (env2,o)
            elif label == 'Until':
                children = s[label]
                e = children[0]
                v = {'Until':children}
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evaluate(env1, e) == 'False':
                    (env2, o1) = execProgram(env1,p1)
                    (env3, o2) = execProgram(env2,v)
                    return (env3, o1 + o2)
                else:
                    (env2, o1) = execProgram(env1, p2)
                    return (env2,o1)               
            elif label == 'Procedure':
                children = s[label]
                v = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[v] = p1
                return execProgram(env, p2)
            elif label == 'Call':
                children = s[label]
                v = children[0]['Variable'][0]
                p = children[1]
                env, e = execProgram(env, env[v])
                if p is not None:
                    env, f = execProgram(env, p)
                    return env, e + f
                else:
                    return env, e

def interpret(s):
	env, out = execProgram({}, tokenizeAndParse(s))
	return out

