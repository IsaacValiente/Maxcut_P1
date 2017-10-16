#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
from solution import Solution
from collections import defaultdict

import local_search
import sys

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

    # nodes, opt_sol, connections = readDataFile("set1/g1.rud")
    nodes, opt_sol, connections = readDataFile("example_set/e1.rud")

    print '\n'
    print '-- graph'
    print("nodes: "+str(nodes))
    print("optimal solution: "+str(opt_sol))
    g = Graph(connections)

    # pprint(g._graph)
    print (g._graph)
    print '--\n'    

    # manual initial solution
    solution = Solution({1}, {2, 3, 4, 5, 6}, 10)
    best = solution._value

    # number of times in a row a worse solution is allowed
    iterations = 5

    print '-- init solution:'
    print solution
    print 'best: ' + str(best)
    print '--\n'

    # best best
    # local_search.best_best(g, solution)

    # first best
    local_search.first_best(g, solution, iterations)
    
    # solution found
    print solution

if __name__ == "__main__":
    main(sys.argv)