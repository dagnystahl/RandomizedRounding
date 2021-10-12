#!/usr/bin/python3

"""
Usage: ./mathematica-parser.py <original input file> <mathematica output>

* This file transforms mathematica's output to the proper output
  as expected by AlgoBOWL
"""

import sys
from RR import read_input_file 

"""
Transforms mathematica's output string (which is a set using { })
to a python int list
"""
def mathematica_parse():
    input_string = ""

    with open(sys.argv[2]) as f:
        input_string = f.readlines()[0]
    
    parsed = input_string.replace("{", "").replace("}", "").split(",")
    parsed = [int(i) for i in parsed]

    return parsed

parsed_solution = mathematica_parse()
sets, weights, n, set_number = read_input_file(sys.argv[1])

weight = 0
final_solution = ""

for i, b in enumerate(parsed_solution):
    if b:
        weight += weights[i]
        final_solution += f"{i} "

print(weight)
print(final_solution)
