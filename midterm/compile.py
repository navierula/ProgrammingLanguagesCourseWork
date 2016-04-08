#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#
# Modified by: Navraj Narula

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
# Complete 'True', 'False', 'Element', and 'Plus' cases for Problem #4.
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)
            elif label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                left, addr1, heap = compileExpression(env, e1, heap)
                right, addr2, heap = compileExpression(env, e2, heap)
                heap = heap + 1
                finSumAddr = heap
                plus = [
                    copy(left, 1),\
                    copy(right, 2),\
                    ['add'],\
                    copy(0, finSumAddr)]
                plus = sum(plus, [])
                return left + right + plus, finSumAddr, heap
            elif label == 'Element':
                c1 = children[0]['Variable']
                addr = env[x]
                exp = children[1]
                (i, a, heap) = compileExpression(env, exp, heap)
                heap = heap + 1
                inst = []
                return inst, heap, heap
    elif type(e) == 'Leaf':
        if e == 'True':
            heap = heap + 1
            addr = heap
            return (['set ' + str(addr) + ' ' + '1'], addr, heap)
        if e == 'False':
            heap = heap + 1
            addr = heap
            return (['set ' + str(addr) + ' ' + '0'], addr, heap)


def compileProgram(env, s, heap = 8): # Set initial heap default address.
    # Complete 'Assign' and 'Loop' cases for Problem #4.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            if label == 'Assign':
                var, c1, c2, c3, pro = children
                var = var['Variable'][0]
                c1Loc, addr1, heap = compileExpression(env, c1, heap)
                c2Loc, addr2, heap = compileExpression(env, c2, heap)
                c3Loc, addr3, heap = compileExpression(env, c3, heap)
                heap = heap + 1
                addr = heap
                env[var] = addr
                assign = [
                    copy(addr1, addr),\
                    copy(addr2, addr + 1),\
                    copy(addr3, addr + 2)
                    ]
                assign = sum(assgin, [])
                env, output, heap = compileProgram(env, pro, heap + 2)
                return env, c1Loc + c2Loc + c3Loc + assign + output, heap
##            if label == 'Loop':
            
def compile(s):
    p = tokenizeAndParse(s)
    val = typeProgram({}, p)
    if val is not None:
        p = eliminateDeadCode(foldConstants(p))
        (env, insts, heap) = compileProgram({}, p)
        return insts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
