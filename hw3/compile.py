######################################################################
#
# CAS CS 320, Fall 2015
# Assignment 3 (skeleton code)
# compile.py
#

# Navraj Narula
# Homework 3
# CS 320 - compile.py

exec(open('parse.py').read())
exec(open('machine.py').read())

from random import randint

def compileExpression(env, e, heap):
    iT, aT, hT = compileTerm(env, e, heap) #instance, address, and heap for term
    iF, aF, hF = compileFormula(env, e, heap) # instance, address, and heap for formula
    if iT is not None:
	    return iT, aT, hT
    elif iF is not None:
	    return iF, aF, hF
    else:
	    return [], None, heap


def compileTerm(env, t, heap):
    if type(t) is dict:
        for label in t:
            children = t[label]
            if label == "Number":
                i, a, heap = storeVal(children[0], heap)
                return i, a, heap
            elif label == "Variable":
                if env[children[0]] is not None:
                    return [], env[children[0]], heap
                else:
                    i, a, heap = storeVal(children[0], heap)
                    return i, a, heap
            elif label == "Plus":
                i1, a1, heap = compileTerm(env, children[0], heap)
                i2, a2, heap = compileTerm(env, children[1], heap)
                iSum, a3, heap = memAdd(a1, a2, heap)
                return i1 + i2 + iSum, a3, heap
    return None, None, None


def compileFormula(env, f, heap):
    if type(f) is dict:
        for label in f:
            children = f[label]
            if label == "And":
                i1, a1, heap = compileFormula(env, children[0], heap)
                i2, a2, heap = compileFormula(env, children[1], heap)
                i3, a3, heap = memAdd(a1, a2, heap)
                i3 += set(1, -1)
                i4, a4, heap = memAdd(1, a3, heap)
                ri = randint(0, 10000000)
                i4 += ['branch setOne'+str(ri) + ' ' + str(a4)]
                i4 += ['goto setZero'+str(ri)]
                i4 += ['label setOne'+str(ri)]
                i4 += set(a4, 1)
                i4 += ['goto afterSet'+str(ri)]
                i4 += ['label setZero'+str(ri)]
                i4 += set(a4, 0)
                i4 += ['label afterSet'+str(ri)]
                return i1 + i2 + i3 + i4, a4, heap
            elif label == "Xor":
                i1, a1, heap = compileFormula(env, children[0], heap)
                i2, a2, heap = compileFormula(env, children[1], heap)
                i3, a3, heap = memAdd(a1, a2, heap)
                ri = randint(0, 10000000)
                i3 += ['branch setOne'+str(ri) + ' ' + str(a3)]
                i3 += ['goto setZero'+str(ri)]
                i3 += ['label setOne'+str(ri)]
                i3 += set(a3, 1)
                i3 += ['goto afterSet'+str(ri)]
                i3 += ['label setZero'+str(ri)]
                i3 += set(a3, 0)
                i3 += ['label afterSet'+str(ri)]
                return i1 + i2 + i3, a3, heap
            elif label == "Not":
                ri = randint(0, 10000000)
                inst, a, heap = compileFormula(env, children[0], heap)
                i = copy(a, heap)
                i += ['branch setZero'+str(ri) + ' ' + str(heap)]
                i += ['goto setOne'+str(ri)]
                i += ['label setZero'+str(ri)]
                i += set(heap, 0)
                i += ['goto afterSet'+str(ri)]
                i += ['label setOne'+str(ri)]
                i += set(heap, 1)
                i += ['label afterSet'+str(ri)]
                return inst + i, heap, heap + 1
            elif label == "Variable":
                if env[children[0]] is not None:
                        return [], env[children[0]], heap
                else:
                        instance, address, heap = storeVal(children[0], heap)
                        return instance, address, heap

    else:
        if f == "True":
                instance, address, heap = storeVal(1, heap)
                return instance, address, heap
        elif f == "False":
                instance, address, heap = storeVal(0, heap)
                return instance, address, heap
    return None, None, None


def compileProgram(env, s, heap):
    if type(s) is dict:
        for label in s:
            children = s[label]
            if label == "Print":
                c1, c2 = children[0], children[1]
                i, a, heap = compileExpression(env, c1, heap)
                h = printMem(a)
                if c2 is not None:
                    if c2 != "End":
                        env, g, heap = compileProgram(env, c2, heap)
                        return env, i + h + g, heap
                    else:
                        return env, i + h, heap
                else:
                        return env, i + h, heap
            elif label == "Assign":
                c1, c2 = children[0]["Variable"][0], children[1]
                i, address, heap = compileExpression(env, c2, heap)
                env[c1] = address
                if len(children) > 2:
                    c3 = children[2]
                    env, i2, heap = compileProgram(env, c3, heap)
                    return env, i + i2, heap
                else:
                    return env, i, heap
            elif label == "If":
                c1, c2 = children[0], children[1]
                instance, address, heap = compileExpression(env, c1, heap)
                ri = randint(0, 10000000)
                instance += ['branch startIf' + str(ri) + ' ' + str(address)]
                instance += ['goto afterIf' + str(ri)]
                instance += ['label startIf' + str(ri)]
                env, instance_, heap = compileProgram(env, c2, heap)
                instance += instance_
                instance += ['label afterIf'+str(ri)]
                if len(children) > 2:
                        c3 = children[2]
                        env, instance_, heap = compileProgram(env, c3, heap)
                        return env, instance + instance_, heap
                else:
                        return env, instance, heap
            elif label == "Until":
                    c1, c2  = children[0], children[1]
                    ri = randint(0, 10000000)
                    instance = ['label untilStart'+str(ri)]
                    #instance = ['label afterLoop' + str(rand_int)] #???
                    instance2, address, heap = compileExpression(env, c1, heap)
                    instance += instance2
                    # if val is c1 != 0, true
                    instance += ['branch endLoop'+ str(ri) + ' ' + str(address)]
                    instance += ['goto afterLoop'+str(ri)]
                    instance += ['label continueLoop'+ str(ri) + ' ' + str(address)]                                          
                    env, instance2, address2 = compileProgram(env, c2, heap)
                   #instance2, address2, heap = compileProgram(env, c2, heap)
                    #print("heap is:",heap)
                    instance += instance2
                    #instance += copy(heap,address2)
                    #instance += copy(address2, address)
                    instance += ['goto untilStart'+str(ri)]
                    instance += ['label endLoop'+str(ri)]
                    if len(children) > 2:
                        c3 = children[2]
                        env, instance2, heap = compileProgram(env, c3, heap)
                        return env, instance + instance2, heap
                    else:
                        return env, instance, heap
            elif label == "Procedure":
                    c1, c2 = children[0]['Variable'][0], children[1]
                    env, body, heap = compileProgram(env, c2, heap)
                    i = procedure(c1, body)
                    if len(children) > 2:
                            c3 = children[2]
                            env, i2, heap = compileProgram(env, c3, heap)
                            return env, i + i2, heap
                    else:
                            return env, i, heap
            elif label == "Call":
                    c1 = children[0]['Variable'][0]
                    i = call(c1)
                    if len(children) > 1:
                            c2 = children[1]
                            env, i2, heap = compileProgram(env, c2, heap)
                            return env, i + i2, heap
                    else:
                            return env, i, heap

    if s == "End":
        return env, [], heap
    


def set(addr, val):
    return ['set ' + str(addr) + ' ' + str(val)]


def compile(s):
    (env, o, heap) = compileProgram({}, tokenizeAndParse(s), 8)
    initial = set(7, 0)
    return initial + o

#eof
