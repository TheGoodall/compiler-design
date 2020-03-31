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
            temp = symbols[i]+"{0}"
            for j in data[i]:
                temp+=(j)+"|"
            P.append(temp[:-1])


    temp = ":P{0}"
    for predicate in data[2]:
        
        m = re.search("\[([0-9]*[1-9])\]", predicate)
        n = re.search("^.*\[", predicate)
        try:
            arity = int(m.group(0)[1:-1])
            name = n.group(0)[0:-1]
            temp += name+"("+":D,"*(arity-1)+":D)|"
        except AttributeError:
            exit(1)
    P.append(temp[:-1])
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
    
    formula += "(:F'|"
    formulap = ":F'{0}"+"R{0}R)|:F:F''".format(equality)
    formula += ":¬:F"
    formulapp = ":F''{0}" + ":N :F)" 
    P.append(vars_const)
    P.append(formulap)
    P.append(formulapp)
    

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
    start = ":S{0}:F"
    P.append(start)
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
    S = ":S"

    return [Vt, Vn, P, S]

def generate_parse_tree(grammer, formula):
    tree = Digraph()
    top = Digraph()
    top.attr(rank="same")

    tree.subgraph(top)
    tree.node("1", label=grammer[3])


    
    
    productions = []

    for part in grammer[2]:
        a = part.split(ARROW)
        startnode = a[0]
        ends = a[1]
        for end in ends.split("|"):
            productions.append("{0}{1}{2}".format(startnode, ARROW, end))
    prods = {}
    for production in grammer[2]:
        prods[production.split(ARROW)[0]] = production.split(ARROW)[1].split("|")
    def parse(formula, prods, index, to_match):
        if formula[index]==to_match:
            return [to_match,None]
        else:
            for production in prods[to_match]:
                for i, term in enumerate(re.findall(r"\:[A-Z¬]\'*|[(,) ]|[\\a-zA-Z=]+", production)):
                    if term == formula[index+i] or production == prods[to_match][-1]:
                        treelist = [term, []]
                        for j, term2 in enumerate(re.findall(r"\:[A-Z¬]\'*|[(,) ]|[\\a-zA-Z=]+", production)):
                            treelist[1].append(parse(formula, prods, index+j, formula[index+j]))
                        return treelist



                        
    a = parse(formula, prods, 0, ":F")
    print(a)

        

    #tree.render("parse_tree", format="png")

FILENAME = "example.txt"
data = readfile(FILENAME)


data = parsedata(data)
a = grammar(data)
with open("grammer.txt", "w") as file_obj:
    stri  = "Non-Terminals: "
    for non_terminal in a[0]:
        stri += non_terminal + ", "
    stri += "\nTerminals:"
    for terminal in a[1]:
        stri += terminal + ", "
    stri += "\nProduction rules:\n"
    for rule in a[2]:
        stri += rule + "\n"

    print(stri)
    


    file_obj.write(stri)
generate_parse_tree(a, data[6])
