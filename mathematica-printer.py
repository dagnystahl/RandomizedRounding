#!/usr/bin/python3
import sys
from RR import read_input_file

def mathematica_solve(sets, weights, n, set_number):
    # Mathematica uses A.x >= b rather than A.x <= b
    A = [[1 if j in s else 0 for s in sets] for j in range(1, n+1)]
    b = [1 for i in range(n)]
    c = weights
    lu = [[0, 1] for i in range(set_number)]
    
    # turns python-style vectors and matrices into mathematica
    def mize(v):
        return str(v).replace('[', '{').replace(']', '}')

    return f"""
        A = {mize(A)};
        c = {mize(c)};
        b = {mize(b)};
        LU = {mize(lu)};
        LinearProgramming[c, A, b, LU, Integers]
    """


sets, weights, n, set_number = read_input_file(sys.argv[1]);
print(mathematica_solve(sets, weights, n, set_number))

