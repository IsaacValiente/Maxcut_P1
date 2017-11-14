from __future__ import division
from solution import Solution
import copy, random, math

###################################################################
# generate_initial
# @param [graph] Graph
# @param [random] Boolean : Use random generation
def generate_initial(graph, rand=False):
    """ Generate initial solution """
    partitionA = set()
    partitionB = set()
    #RANDOM
    if rand:
        for node in graph._graph:
            if random.randint(0,1) == 0:
                partitionA.add(node)
            else:
                partitionB.add(node)
    #GREEDY
    else:
        for node in graph._graph:
            wAwB = weight(graph,partitionA,partitionB,node)
            if wAwB > 0:
                partitionA.add(node)
            else:
                partitionB.add(node)

    cutValue = totalCutValue(graph, partitionA, partitionB)

    return Solution(partitionA, partitionB, cutValue)
    # return (partitionA,partitionB)

###################################################################
# weight
# @param [graph] Graph
# @param [A] Set of nodes : partitionA
# @param [B] Set of nodes : partitionB
# @param [v] vertex
def weight(graph,A,B,v):
    wvb = 0
    wva = 0
    #WvB
    for b in B:
        if graph.is_connected(v,b):
                wvb = wvb + graph.weight(v,b)
    #WvB
    for a in A:
        if graph.is_connected(v,a):
            wva = wva + graph.weight(v,a)    
    return wvb - wva


###################################################################
# totalCutValue
def totalCutValue(graph, A, B):
    """ Get the total value of the Cut """
    cutWeight = 0
    for a in A:
        for b in B:
            if graph.is_connected(a,b):
                cutWeight = cutWeight + graph.weight(a,b)
    return cutWeight
  
  
def cut_value(graph, solution, candidate):
    """ Calculate weight of the solution if a candidate is added to the cut """
    
    # current weight of cut solution
    cutWeight = solution._value

    connections = graph._graph[candidate]
    partitionA = solution._partitionA
    
    for connection in connections:
        # print connection[0]
        if (connection[0]) in (partitionA):
            cutWeight -= connection[1]    
        else:
            cutWeight += connection[1]
    
    return cutWeight