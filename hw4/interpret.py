#####################################################################
#
# CAS CS 320, Fall 2015
# Assignment 4 (skeleton code)
# interpret.py
#
# Written by: Navraj Narula
# November 12, 2015
# Declarative Programming Languages

exec(open('parse.py').read())

Node = dict
Leaf = str

# simply made to retrieve label from dictionary
def retrieveLabel(dictionary):
    """This helper function will retrieve the label in
       the intended dictionary."""
    for label in dictionary:
        return label
    
def subst(s, a):
    """
    takes two arguments: a substitution s (represented as a Python dictionary),
    and an abstract syntax tree a. The function should return a new abstract
    syntax tree in which every variable in the tree that is in the domain
    of s has been substituted according to the substitution s. You may assume
    that variables are always represented using a subtree of the
    form {"Variable":[ ... ]}, as in all previous examples and assignments.
    """

    if type(a) == Leaf:
        return a
    elif type(a) == int:
        return a
    # check to see if sub is valid
    else:
        label = retrieveLabel(a)
        children = a[label]
        if label != 'Variable':
            return {label: [subst(s, a) for a in children]}
        var = children[0]
        try:
            return s[var]
        except:
            return a


def unify(a, b):
    """
     takes two arguments: two syntax trees a and b. The function should
     return the smallest substitution s that satisfies the following equation:

     subst(s, a) == subst(s, b)
              
     You should implement the pattern matching unification algorithm
     for this assignment.

     unify(a, b): two abstract syntax trees a and b
     if both a and b are leaf nodes and are equivalent
         return the empty substitution 0
     if a is a variable node representing a variable x
         return the substitution {x  b}
     if b is a variable node representing a variable x
         return the substitution {x  a}
     if both a and b have the same label and the same number of children
          in order from left to right, unify each pair of corresponding
          children of a and b
          as long as they do not overlap on any variables, combine the
          substitutions obtained above
          return the combined substitution

    """


    # Obtain the label of the root node
    if type(a) == Node and type(b) == Node:
       # print(type(a.keys()),a.keys())
        labelA = retrieveLabel(a)
        labelB = retrieveLabel(b)

    # Covert types (ints, booleans) to string type
    if type(a) != Node:
        a = str(a)
    if type(b) != Node:
        b = str(b)

    # Case 1: If a and b are leaf nodes and they are
    # equivalent to one another, return the empty
    # substitution

    if type(a) == Leaf and type(b) == Leaf:
        if a == b:
            return {}
        else:
            return None

    # Case 2: if a is a variable node representing a variable x
    # return the substitution {x  b}

    if (type(a) == Node and 'Variable' in a) and (type(b) == Node and 'Variable' in b):
        if a['Variable'][0] == b['Variable'][0]:
            return None

    if type(a) == Node and 'Variable' in a:
        dictName = a['Variable'][0]
        return {dictName: b}
    

    # Case 3: if b is a variable node representing a variable x
    # return the substitution {x  a}

    if type(b) == Node and 'Variable' in b:
        dictName = b['Variable'][0]
        return {dictName: a}


    # Case 4: if both a and b have the same label and the same
    # number of children in order from left to right,
    # unify each pair of corresponding children of a and b
    # as long as they do not overlap on any variables, combine the
    # substitutions obtained above
    # return the combined substitution
    
    labelA = retrieveLabel(a)
    labelB = retrieveLabel(b)
    if labelA == labelB and len(a[labelA]) == len(b[labelB]):

            substitution = None

            for i in range(0, len(a[labelA])):
                
                unification = unify(a[labelA][i], b[labelB][i])

                # Check to see if a unification has been found
                if not unification == None:
                    # Perform substitution
                    if substitution == None:
                       # return None
                        substitution = unification

                    else:
                        # Necessary! Check to see for overlapping
                        # variable names (i.e. x = 1, x = 2, etc.)
                        if len(set(unification.keys()) & set(substitution.keys())) != 0:
                            return None
                        substitution.update(unification)
                        
            return substitution

def build(m, d):
    """
    takes a finite map m (i.e., a Python dictionary mapping names to lists
    of (pattern, expression) tuples) and a declaration parse tree d.
    The function should return the finite map m that represents the module
    definition that is assembled according to the operational semantics
    presented
    """
    if type(d) == Node:
        for label in d:
            children = d

    if type(d) == Node:
        for label in d:
            children = d[label]

            name = children[0]["Variable"][0]
            pat = children[1]
            exp = children[2]
            rest = children[3]

            new = (pat, exp)

            if name in m:
                m[name] += [new]
            else:
                m.update({name: [new]})

            return build(m, rest)
    elif type(d) == Leaf:
        if d == "End":
            return m
            
def evaluate(m, env, e):
    """
    takes a module m, an environment env, and an expression abstract
    syntax tree e as its three arguments. The function should return
    the value that corresponds to the evaluation of the abstract syntax
    tree e, as determined by the operational semantics presented below.
    Note that the [Expression-Apply] requires using a unification algorithm
    to obtain a substitution  that unifies p and v1.
    """

    # retrieve label names from test cases
    
    if type(e) == Node:
        for label in e:
            children = e[label]

            if label == 'Number':
                return children[0]

            elif label == 'ConBase':
                return e

            elif label == 'ConInd':
                exp = children[0]
                val1 = evaluate(m, env, children[1])
                val2 = evaluate(m, env, children[2])
                return {'ConInd': [exp, val1, val2]}

            elif label == 'Mult':
                e1 = children[0]
                n1 = evaluate(m, env, e1)
                e2 = children[1]
                n2 = evaluate(m, env, e2)
                return n1 * n2

            elif label == 'Apply':
                e1 = children[0]['Variable'][0]
                v1 = evaluate(m, env, children[1])

                if e1 in m:
                    for i in m[e1]:
                        substitution = unify(v1, i[0])

                        if not substitution == None:
                            env.update(substitution)
                            return evaluate(m, env, i[1])
                        
            elif label == 'Variable':
                var = children[0]
                if var in env:
                    return env[var]
                else:
                    exit()
    # base cases!
    if type(e) == 'Leaf':
        if e == 'True':
            return True
        if e == 'False':
            return False


def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof
