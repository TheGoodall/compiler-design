"""
Compiler design coursework

A program to satisfy the requirements of the compiler design coursework
"""

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
    
    for line in data:
        line = line.strip().split()
        line = [part.strip() for part in line]


    return variables, constants, predicates, equality, connectives, quantifiers, formula

FILENAME = "example.txt"
data = readfile(FILENAME)
parsedata(data)
