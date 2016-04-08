#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#
# Modified by: Navraj Narula

exec(open('parse.py').read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'TyBoolean'

    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'TyNumber'

            elif label == 'Variable':
                el = children[0]
                if e1 in env:
                    if not env[e1] == 'TyNumber':
                        return None
                    else:
                        return 'TyNumber'
                else:
                    return None

            elif label == 'Element':
                c1, c2 = children
                c1Left = typeExpression(env, c1)
                c2Right = typeExpression(env, c2)
                if c1Left == 'TyNumber' and c2Right == 'TyNumber':
                    return 'TyNumber'
                
            elif label == 'Plus':
                c1, c2 = children
                c1Left = typeExpression(env, c1)
                c2Right = typeExpression(env, c2)
                if c1Left == 'TyNumber' and c2Right == 'TyNumber':
                    return 'TyNumber'

def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'TyVoid'
    elif type(s) == Node:
        for label in s:
            
            if label == 'Print':
                [e, p] = s[label]
                expType = typeExpression(env, e)
                expPro = typeExpression(env, p)
                if expType == 'TyNumber' and expProgram == 'TyVoid' or expType == 'TyBoolean' and expPro == 'TyVoid':
                    return 'TyVoid'
                
            if label == 'Assign':
                [xTree, e0, e1, e2, p] = s[label]
                x = xTree['Variable'][0]
                if typeExpression(env, e0) == 'TyNumber' and typeExpression(env, e1) == 'TyNumber' and typeExpression(env, e2) == 'TyNumber':
                    env[x] == 'Element'
                    if typeProgram(env, p) == 'TyVoid':
                        return 'TyVoid'
                
            if label == 'Loop':
                [xTree, nTree, p1, p2] = s[label]
                x = xTree['Variable'][0]
                n = nTree['Number'][0]
                pro1 = typeProgram(env, p1)
                pro2 = typeProgram(env, p2)
                if pro1 == 'TyVoid' and pro2 == 'TyVoid':
                    return 'TyVoid'
                else:
                    return None


#eof
