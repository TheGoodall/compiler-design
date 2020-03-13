"""
Compiler design coursework

A program to satisfy the requirements of the compiler design coursework
"""

import re
from graphviz import Digraph
ARROW = "→"

def readfile(filename):
    """ Reads the file from the filename passed in and returns the data in an array line for line"""
    data = []

    with open(filename, "r") as file_obj:
        for line in file_obj:
            data.append(line)

    return data



def parsedata(data):
    """
    Reads the data and parses it into variables
    """
    variables = []
    constants = []
    predicates = []
    equality = []
    connectives = []
    quantifiers = []
    formula = []
    
    data_copy = []

    for line in data:
        line = line.strip().split()
        line = [part.strip() for part in line]
        data_copy.append(line)
    
    data = []
    for i, line in enumerate(data_copy):
        if ":" in line[0]:
            data.append(line)
        else:
            if i == 0:
                exit(1)
            data[-1].extend(line)
    for line in data:
        if line[0] == "variables:":
            variables.extend(line[1:])
        if line[0] == "constants:":
            constants.extend(line[1:])
        if line[0] == "predicates:":
            predicates.extend(line[1:])
        if line[0] == "equality:":
            equality.extend(line[1:])
        if line[0] == "connectives:":
            connectives.extend(line[1:])
        if line[0] == "quantifiers:":
            quantifiers.extend(line[1:])
        if line[0] == "formula:":
            formula.extend(line[1:])
    formula2 = []
    pattern = re.compile("[(,)]|[^(,)]+")
    for term in formula:
        for match in re.findall(pattern, term):

            formula2.append(match)

    return [variables, constants, predicates, equality, connectives, quantifiers, formula2]

def grammar(data):
    P = [
            ]
    
    symbols = [":V",":C", ":P"]
    for i in range(2):
        if len(data[i]) == 1:
            symbols[i] = data[i][0]
        elif len(data[i]) == 0:
            symbols[i] = ""
        else:
            for j in data[i]:
                P.append(symbols[i]+"{0}"+j)

    
    for predicate in data[2]:
        
        m = re.search("\[([0-9]*[1-9])\]", predicate)
        n = re.search("^.*\[", predicate)
        try:
            arity = int(m.group(0)[1:-1])
            name = n.group(0)[0:-1]
            P.append(":P{0}"+name+"("+":D,"*(arity-1)+":D)")
        except AttributeError:
            exit(1)
    equality = data[3][0]
    


    formula = ":F{0}"
    vars_const = ":D{0}"
    if symbols[0]:
        vars_const += ("{0}").format(symbols[0])
        formula += ":Q {0} :F|".format(symbols[0]) 
    if symbols[1]:
        vars_const += "|{0}".format(symbols[1])
    if symbols[2]:
        formula += "{0}|".format(symbols[2]) 
    if symbols[0] and symbols[1]:
        formula += "(:D {1} :D)|".format(symbols[1], equality, symbols[0])
    elif symbols[0]:
        formula += "({0} {1} {0})|".format(symbols[1], equality, symbols[0])
    elif symbols[1]:
        formula += "({2} {1} {2})|".format(symbols[1], equality, symbols[0])
    
    formula += "(:F :N :F)|"
    formula += ":¬:F"
    P.append(vars_const)
    

    P.extend([
            formula,
            ])

    connective = ":N{0}"
    
    for i in range(4):

        connective += "{0}|".format(data[4][i])

    connective = connective[0:-1]
    P.append(connective)
    negation = ":¬{0}" + "{0}".format(data[4][4])
    P.append(negation)
    
    quantifiers = ":Q{0}" + "{0}|{1}".format(data[5][0], data[5][1])
    P.append(quantifiers)


    P = [rule.format(ARROW) for rule in P]
    
    Vn = [":F", ":Q", ":V", ":N", ":¬", ":C", ":P", ":="]
    Vt = []
    Vt.extend(data[0])
    Vt.extend(data[1])
    Vt.extend(data[2])
    Vt.extend(data[3])
    Vt.extend(data[4])
    Vt.extend(data[5])
    Vt.extend([",", " ", "(", ")"])
    S = ":F"

    return [Vt, Vn, P, S]

def generate_parse_tree(grammer, formula):
    tree = Digraph()
    top = Digraph()
    top.attr(rank="same")

    tree.subgraph(top)
    tree.node("1", label=grammer[3])

    

    print(formula)   
    print(grammer[2])
    
    pt = [[-1 for i in range(len(grammer[0]))] for j in range(len(grammer[1]))]
    
    def get_productions(node):
        productions = []
        pattern = re.compile("\:[A-Z¬]|[(,) ]|[\\a-zA-Z=]+")
        for production in grammer[2]:
            productionsplit = production.split(ARROW)
            if node == productionsplit[0]:
                for RHS in productionsplit[1].split("|"):
                    RHSproduct = []
                    for product in re.findall(pattern, RHS):
                        RHSproduct.append(product)
                    productions.append(RHSproduct)
        return productions

    def first(node):
        
        return []

    def follow(node):
        return []
    

    for row in pt:
        print(row)
    print(get_productions(":F"))

    for lookahead in formula:
        pass

    tree.render("parse_tree", format="png")

FILENAME = "example.txt"
data = readfile(FILENAME)

data = parsedata(data)
a = grammar(data)
generate_parse_tree(a, data[6])
