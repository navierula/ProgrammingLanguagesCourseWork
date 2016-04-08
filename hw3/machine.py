#####################################################################
#
# CAS CS 320, Fall 2015
# Assignment 3 (skeleton code)
# machine.py
#

# Navraj Narula
# CS 320
# Homework 3 - machine.py

def simulate(s):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
    control = 0
    outputs = []
    while control < len(instructions):
        mem[6] = control 
        inst = instructions[control]
        if inst[0] == 'label':
            pass
        if inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'branch' and mem[int(inst[2])]:
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        if inst[0] == 'set':
            mem[int(inst[1])] = int(inst[2])
        if inst[0] == 'copy':
            mem[mem[4]] = mem[mem[3]]
        if inst[0] == 'add':
            mem[0] = mem[1] + mem[2]
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1
        control = control + 1

    print("memory: "+str(mem))
    return outputs
   
def copy(frm, to):
   return [\
      'set 3 ' + str(frm),\
      'set 4 ' + str(to),\
      'copy'\
   ]

def increment(addr):
    inst = [\
        ['set 1 1'],\
        copy(addr, 2),\
        ['add'],\
        copy(0, addr)\
        ]
    for i in range(5):
        inst.append(['set '+ str(i) + " 0"])
    return sum(inst, [])

def decrement(addr):
    inst = [\
        ['set 1 -1'],\
        copy(addr, 2),\
        ['add'],\
        copy(0, addr)\
        ]
    for i in range(5):
        inst.append(['set '+ str(i) + " 0"])
    return sum(inst, [])

def call(name):
    inst = [
            decrement(7),\
            copy(6, 1),\
            ['set 2 9'],\
            ['add'],\
            copy(7, 4),\
            ['set 3 0'],\
            ['copy'],\
            ['goto ' + name],\
            increment(7)
    ]
    return sum(inst, [])


def procedure(name, body):
    startLabel = name
    endLabel = name + "_end"
    inst = [
            ['goto ' + endLabel],\
            ['label ' + startLabel],\
            body,\
            copy(7, 3),\
            ['set 4 0'],\
            ['copy'],\
            ['jump 0'],\
            ['label ' + endLabel]\
    ]
    return sum(inst, [])

# Separate helper functions (to ease the process in compile)

def storeVal(v, a):
    inst = ["set " + str(a) + " " + str(v)]
    return inst, a, a + 1


def assignVal(a, v):
    inst = ["set " + str(a) + " " + str(v)]
    return a, a + 1, inst


def memAdd(a, a2, heap):
    inst = [
            copy(a, 1),
            copy(a2, 2),
            ["add"],
            copy(0, heap)
    ]
    inst = sum(inst, [])
    return inst, heap, heap + 1

def printVal(v):
    inst = ['set 5 ' + str(val)]
    return inst


def printMem(v):
    inst = copy(str(v), 5)
    return inst


# eof
