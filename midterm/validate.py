#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#
# Modified by: Navraj Narula

exec(open('analyze.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())

def convertValue(v):
    if type(v) == Leaf:
        if v == 'True':
            return 1
        if v == 'False':
            return 0
    if type(v) == Node:
        for label in v:
            return 1 + max([convertValue(child) for child in v[label]])

# Converts an output (a list of values) from the
# value representation to the machine representation
def convert(o):
    return [convertValue(v) for v in o]

def expressions(n):
    if n <= 0:
        []
    elif n == 1:
         # Add all base case(s) for Problem #5.
         # The only possible element variable name is 'a.'
        return ['True','False',{'Element': [{'Variable': ['a']}, {'Number': [1]}]},{'Element': [{'Variable': ['a']}, {'Number': [1]}]},{'Element': [{'Variable': ['a']}, {'Number': [1]}]}]
    else:
        # Add recursive case(s) for Problem #5.
        exp = expressions(n-1)
        expVal = []
        return exp + expVal

def programs(n):
    if n <= 0:
        []
    elif n == 1:
        return ['End'] 
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        # Add more nodes to psN for Problem #5.
        psN = psN + [{'Assign':[{'Variable':['a']}, exp, exp, exp, pro]} for pro in ps for exp in es]
        psN = psN + [{'Print': [exp, pro]} for exp in es for pro in ps]
        psN = psN + [{'Loop': [{'Variable':['x']},pro1, pro2]} for pro1 in ps for pro2 in ps]
        return ps + psN
   
# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most k.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def exhaustive(k):
    for p in programs(4):
        try:
            if simulate(compile(p)) != convert(execute(p)):
                print('\nIncorrect behavior on: ' + str(p))
        except:
            print('\nError on: ' + str(p))

#eof
