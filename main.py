#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
import sys
import time
from tabu import tabuSearch, annealing
from local_search import generate_initial, totalCutValue

##############################################
# Print Graph
# PYTHON3 needed
# def pprint(g):
#     print("{'", end="")
#     first = True
#     for node in g:
#         if first:
#             first = False
#             print (str(node)+"': {", end="")
#         else:
#             print ("  "+str(node)+"': {", end="")
#         ffirst = True
#         for n,w in g[node]:
#             if ffirst:
#                 ffirst = False
#                 print ("("+str(n)+","+str(w)+")",end="")
#             else:
#                 print (",("+str(n)+","+str(w)+")",end="")
#         print("}")
#     print("}")

##############################################
# Read file
# @param [File] filename : file with data
def readDataFile(filename):
    nodes = 0
    opt_sol = 0
    connections = []

    # with open(filename, 'r', encoding="utf-8") as data_file:
    with open(filename, 'r') as data_file:        
        first = True
        for line in data_file:
            _line = line.rstrip().split(" ")
            if first:
                first = False
                opt_sol = int(_line.pop())
                nodes = int(_line.pop())
            else:
                l = tuple([ int(li) for li in _line ])
                connections.append(l)
    return nodes, opt_sol, connections

##############################################
# MAIN        

def main(argv):
    start = time.time()
    nodes, opt_sol, connections = readDataFile("set1/g44.rud")
    g = Graph(connections)
    initial_solution = generate_initial(g,False)
    # print("INITIAL SOLUTION: "+str(initial_solution))
    maxIWoImp = 5000
    neighSize = nodes
    minTIter = 2
    maxTIter = 3
    # sol = tabuSearch(maxIWoImp, g, initial_solution._partitionA, initial_solution._partitionB, neighSize, minTIter, maxTIter)

    temp = 50000
    A = 200
    K = 2000
    maxIWoImpSA = 10
    sol = annealing(maxIWoImpSA, g, initial_solution._partitionA, initial_solution._partitionB, K, A, temp, initial_solution._value, neighSize)
    end = time.time()
    print('elapsed time: '+str(end - start))

if __name__ == "__main__":
    main(sys.argv)
