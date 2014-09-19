#!/usr/bin/python

from __future__ import division
import numpy
import time

def print_matrix(matrix_type, matrix):
    if matrix_type == "float":
        for row in matrix:
            print " ".join("%.2f" % v for v in row)
    elif matrix_type == "dos":
        for row in matrix:
            print " ".join([" ", ".", "+", "X", "O"][v] if v < 4 else str(v) 
                           for v in row)

params = { "N": 20,
           "threshold": 0.8,
           "training_delta": 1,
           "target_dos": 3,
           "dos_cost_mult": 3,
           "power_law_cost": 1,
           }

# @param n {int} Get the number of elements in the upper triangular matrix
def triu_length(n):
    return n * (n + 1) / 2

# @param i {int} The starting node
# @param j {int} The target node
def get_dos(N, i, j):
    already_hit = set()
    stack = [(0, i)]
    while len(stack) != 0:
        depth, current_node = stack.pop()
        if current_node == j:
            return depth
        for next_node, value in enumerate(N[current_node]):
            if value > params["threshold"]:
                if next_node not in already_hit:
                    stack.append((depth + 1, next_node))
                    already_hit.update([next_node])
    return -1

num_nodes = 20
N = numpy.random.rand(params["N"], params["N"])
N += N.T
numpy.fill_diagonal(N, 0)

print_matrix("float", N)
print

prev_average_dos = None

while True:
    dos = numpy.array([[get_dos(N, i, j) for j in range(params["N"])]
                       for i in range(params["N"])])
    
    print_matrix("dos", dos)
    print
    
    average_dos = numpy.triu(dos).sum() / triu_length(params["N"])
    print "Average DOS:", average_dos
    
    if prev_average_dos == average_dos:
        break
    prev_average_dos = average_dos
    
    multiplier = dos - params["target_dos"]
    error = params["target_dos"] - average_dos
    N += multiplier * params["training_delta"] * error
    
    max_value = max(map(max, N))
    min_value = min(map(min, N))
    print min_value, max_value
    N -= min_value
    N /= max_value - min_value
    
    print_matrix("float", N)
    
    time.sleep(1)

