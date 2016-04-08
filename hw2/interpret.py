exec(open('parse.py').read())

#Name: Navraj Narula
#CS320 HW2: Parsing Algorithms and Interpreters
#Oct. 2, 2015

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

Node = dict
Leaf = str

def evaluate(env, p):
    if not evalTerm(env,p) == None:
        return evalTerm(env,p)
    else:
        return evalFormula(env,p)

def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'If':
                f = children[0]
                t1 = children[1]
                t2 = children[2]
                if evalFormula(env, f) == 'True':
                    v1 = evalTerm(env, t1)
                    return v1
                else:
                    v2 = evalTerm(env, t2)
                    return v2
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Number':
                
                x = children[0]
                return {'Number': [x]}
                
            elif label == 'Parens':
                t = children[0]
                v = evalTerm(env, t)
                return v
            elif label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                return {'Number':[v1['Number'][0] + v2['Number'][0]]}
            elif label == 'Mult':
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                return {'Number':[v1['Number'][0] * v2['Number'][0]]}
    else:
        return None

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
                if v['Number'][0] != 0:
                    return 'True'
                if v['Number'][0] == 0:
                    return 'False'
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
    elif type(f) == Leaf:
        if f == 'True':
            return 'True' 
        if f == 'False':
            return 'False' 
    else:
        return None

def execProgram(env,s):

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
                x = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                v = evaluate(env, e)
                env[x] = v
                (env2, o) = execProgram(env, p)
                return (env2, o)
            if label == 'If':
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evaluate(env,e)
                if v == 'False':
                    (env2, o1) = execProgram(env, p2)
                    return (env2, o1)
                else:
                    (env2, o1) = execProgram(env, p1)
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)

            if label == 'DoUntil':
                children = s[label]
                p1 = children[0]
                e = children[1]
                p2 = children[2]
                env1 = env
                

                (env2, o1) = execProgram(env1, p1)
                if evaluate(env2, e) == 'True':
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)
                elif evalaute(env2, e) == 'False':
                    (env3, o2) = execProgram(env2, {'DoUntil':[p1,e,p2]})
                    return (env3, o1 + o2)
    else:
        return None
                

def interpret(s):
    tlist = ['and', 'nonzero',"not","true", \
             "false","\+","\*","if", \
             "\(","\)","print","assign","if","do", \
             "\{","\}", "until", ",", ";",":=",'[0-9]+', '[A-Za-z]+']
    tokens = tokenize(tlist,s)

    result = program(tokens) 
    if result is not None:
        output = execProgram({},result[0])
        return output[1]
    else:
        return None
        
        
        
    
