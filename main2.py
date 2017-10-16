#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
from solution import Solution
from collections import defaultdict
from local_search import generate_initial, totalCutValue

import local_search
import sys

##############################################
# Print Graph
# PYTHON3 needed
'''
def pprint(g):
    print("{'", end="")
    first = True
    for node in g:
        if first:
            first = False
            print (str(node)+"': {", end="")
        else:
            print ("  "+str(node)+"': {", end="")
        ffirst = True
        for n,w in g[node]:
            if ffirst:
                ffirst = False
                print ("("+str(n)+","+str(w)+")",end="")
            else:
                print (",("+str(n)+","+str(w)+")",end="")
        print("}")
    print("}")
'''
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

    # check command usage
    if len(argv) < 3:
        print 'usage error: arguments required'
        print 'argv[1]: number of solutions to test'
        print 'argv[2]: improvement type'
        print '         1: first best'
        print '         2: best best'
        print '         3: percentage best'
        print 'argv[3]: improvement type argument'
        print '         first best: max iteration number'
        print '         percentage best: percentage'
        return
    else:
        # number of solutions
        solutionNumber = int(argv[1])
        if argv[2] == '1':
            if len(argv) < 3:
                print 'usage error: max iterarion number required'
                return
            else:
                iterations = int(argv[3])
        elif argv[2] == '3':
            if len(argv) < 3:
                print 'usage error: percentage required'
                return
            else:
                percentage = int(argv[3])
        elif int(argv[2]) > 3:
            print 'usage error: improvement type ' + argv[2] + ' not found'
            return

    # nodes, opt_sol, connections = readDataFile("set1/g1.rud")
    nodes, opt_sol, connections = readDataFile("example_set/e1.rud")

    #print '\n'
    #print '-- graph'
    print("nodes: "+str(nodes))
    print("optimal solution: "+str(opt_sol))
    g = Graph(connections)

    # initial solutions list
    initSolutions = []
    best = []
    for i in range(solutionNumber):
        #RANDOM
        initial_solution = generate_initial(g,True)
        #GREEDY
        # initial_solution = generate_initial(g)
        # print("INITIAL SOLUTION: "+str(initial_solution))
        initSolutions.append(initial_solution)
    
    print '-- solution list (x' + str(solutionNumber) + ')'
    for sol in initSolutions:
        print sol
        print '-'
    print '--\n'

    # local search solution improvement type:
    # 1. first best (argv[2]: max iteration number)
    #    max iteration number: of times in a row a worse solution is allowed
    # 2. best best
    # 3. percentage best (argv[2]: percentage)
    if argv[2] == '1':
        for solution in initSolutions:
            local_search.first_best(g, solution, iterations)
            best.append(solution._value)
            print solution

    elif argv[2] == '2':
        local_search.best_best(g, initSolutions[0]) 
        best.append(initSolutions[0]._value)
        print initSolutions[0]
        
    elif argv[2] == '3':
        for solution in initSolutions:
            local_search.percentage_best(g, solution, percentage)
            best.append(solution._value)
            print solution

    # best solutions list
    print best

if __name__ == "__main__":
    main(sys.argv)