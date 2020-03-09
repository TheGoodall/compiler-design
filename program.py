"""
Compiler design coursework

A program to satisfy the requirements of the compiler design coursework
"""
def readfile(filename):
    """ Reads the file from the filename passed in and returns the data in an array line for line"""
    data = []

    with open(filename, "r") as file_obj:
        for line in file_obj:
            data.append(line)

    return data



