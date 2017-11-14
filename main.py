#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
import sys
from tabu import TabuSearch, CompTabuSearch, annealing
from local_search import generate_initial, totalCutValue
import time
from numpy import inf
from math import pow, sqrt


# mean
def a_Time(xsolution):
    avg_time = 0
    for s in xsolution:
        avg_time += s[1]
    avg_time = avg_time / len(xsolution)
    return avg_time

##############################################

# mean
def mean(xsolution):
    meanv = 0
    for s in xsolution:
        meanv += s[0]._value
    meanv = (meanv / len(xsolution))
    return meanv

##############################################

# mean
def desvStd(xsolution, mean):
    desv = 0
    for s in xsolution:
        desv += pow((s[0]._value - mean),2)
    desv = desv / len(xsolution)
    desv = sqrt(desv)
    return desv

##############################################

# mean
def min(xsolution):
    minv = inf
    for s in xsolution:
        if s[0]._value < minv:
            minv = s[0]._value
    return minv

##############################################

# mean
def max(xsolution):
    maxv = -inf
    for s in xsolution:
        if s[0]._value > maxv:
            maxv = s[0]._value
    return maxv

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
    problem = sys.argv[1]
    search = sys.argv[2]
    print("\n################# "+problem+" #################\n")
    nodes, opt_sol, connections = readDataFile("set1/"+problem)
    g = Graph(connections)
    initial_solution = generate_initial(g,False)

    if (search == 'T'):
        print("## TABU ##")
        ##############################################
        # TABU

        maxIWoImp = 5000
        neighSize = nodes
        minTIter = 25
        maxTIter = 100
        start_time = time.time()
        sol_fb = []
        sol_porc = []
        sol_ct = []
        sol_bb = (TabuSearch(maxIWoImp, g, initial_solution._partitionA, initial_solution._partitionB, neighSize, minTIter, maxTIter, 100, False),time.time() - start_time)
        for i in range(0,10):
            start_time = time.time()
            sol_fb.append((TabuSearch(maxIWoImp, g, initial_solution._partitionA, initial_solution._partitionB, neighSize, minTIter, maxTIter, 100, True),time.time() - start_time))
            start_time = time.time()
            sol_porc.append((TabuSearch(maxIWoImp, g, initial_solution._partitionA, initial_solution._partitionB, neighSize, minTIter, maxTIter, 70, False),time.time() - start_time))
            start_time = time.time()
            sol_ct.append((CompTabuSearch(maxIWoImp, g, initial_solution._partitionA, initial_solution._partitionB, neighSize, minTIter, maxTIter),time.time() - start_time))        
        

        print("##### Best #####")

        print("\tValue: "+str(sol_bb[0]._value))
        print("\tTime: "+str(sol_bb[1]))

        print("##### FirstBest #####")

        meanv = mean(sol_fb)
        maxv = max(sol_fb) 
        minv = min(sol_fb)
        desv = desvStd(sol_fb, meanv)
        avgTime = a_Time(sol_fb)

        print("\tMean: "+str(meanv))
        print("\tMax: "+str(maxv))
        print("\tMin: "+str(minv))
        print("\tAvgTime: "+str(avgTime))
        print("\tDesv: "+str(desv))

        print("##### 70% #####")

        meanv = mean(sol_porc)
        maxv = max(sol_porc) 
        minv = min(sol_porc)
        desv = desvStd(sol_porc, meanv)
        avgTime = a_Time(sol_porc)

        print("\tMean: "+str(meanv))
        print("\tMax: "+str(maxv))
        print("\tMin: "+str(minv))
        print("\tAvgTime: "+str(avgTime))
        print("\tDesv: "+str(desv))    

        print("##### CompetitiveTabu #####")

        meanv = mean(sol_ct)
        maxv = max(sol_ct) 
        minv = min(sol_ct)
        desv = desvStd(sol_ct, meanv)
        avgTime = a_Time(sol_ct)

        print("\tMean: "+str(meanv))
        print("\tMax: "+str(maxv))
        print("\tMin: "+str(minv))
        print("\tAvgTime: "+str(avgTime))
        print("\tDesv: "+str(desv))    

    elif (search == 'A'):
        print("## Simulated Annealing ##")
        ##############################################
        # SIMULATED ANNEALING

        temp = 50000
        A = 200
        K = 2000
        maxIWoImpSA = 10
        neighSize = nodes

        # SA execution
        start = time.time()
        sol = annealing(maxIWoImpSA, g, initial_solution._partitionA, initial_solution._partitionB, K, A, temp, initial_solution._value, neighSize)
        end = time.time()

        elapsed = end - start
        print('elapsed time: '+str(elapsed)+'\n')
    
    else:
        print('T: TABU | A: Simulated Annealing')

if __name__ == "__main__":
    main(sys.argv)
