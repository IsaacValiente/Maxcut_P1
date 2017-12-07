#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
import sys
import time
from numpy import inf
from math import pow, sqrt
from scatterSearch import scatterSearch


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
    print("################# "+problem+" #################")
    nodes, opt_sol, connections = readDataFile("set1/"+problem)
    graph = Graph(connections)

    alpha = 0.25
    b = 10
    start_time = time.time()
    sol = []
    for i in range(0,5):
        start_time = time.time()
        sol.append(( scatterSearch(graph, alpha, b) ,time.time() - start_time))

    print("##### ScatterSearch #####")
    print("b = "+str(b))
    print("alpha = "+str(alpha))
    meanv = mean(sol)
    maxv = max(sol) 
    minv = min(sol)
    desv = desvStd(sol, meanv)
    avgTime = a_Time(sol)

    print("\tMean: "+str(meanv))
    print("\tMax: "+str(maxv))
    print("\tMin: "+str(minv))
    print("\tAvgTime: "+str(avgTime))
    print("\tDesv: "+str(desv))    


if __name__ == "__main__":
    main(sys.argv)