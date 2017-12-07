from __future__ import division
from solution import Solution
import copy, random, math

###################################################################
# generate_initial
# @param [graph] Graph
# @param [random] Boolean : True for random generation false for greedy
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
# weight
# @param [graph] Graph
# @param [A] Set of nodes : partitionA
# @param [B] Set of nodes : partitionB
def totalCutValue(graph, A, B):
    """ Get the total value of the Cut """
    cutWeight = 0
    for a in A:
        for b in B:
            if graph.is_connected(a,b):
                cutWeight = cutWeight + graph.weight(a,b)
    return cutWeight

############################################################################
# totalCutValue
# @param [graph] Graph
# @param [S] Set of nodes : partitionA
# @param [Sp] Set of nodes : partitionB
def totalCutValue(graph, S, Sp):
    """ Get the total value of the Cut """
    cutWeight = 0
    for node in S:
        connect_node = graph._graph[node]
        for c in connect_node:
            if c[0] in Sp:
                cutWeight = cutWeight + c[1]
    return cutWeight
  
    
############################################################################
# cut_value : Calculate weight of the solution if a candidate is added to the cut
# @param [graph] Graph
# @param [random] Boolean : Use random generation
def cut_value(graph, S, SP, total, node, check_node_origin):
    wn = 0
    wnS = 0
    wnSp = 0

    connect_n = graph._graph[node]
    for c in connect_n:
        if c[0] in S:
            wnS += c[1]
        else:
            wnSp += c[1]

    wn = wnSp - wnS
    if check_node_origin and (node in S):
        wn = wnS -wnSp

    return total+wn


############################################################################

########################IMPROVEMENT METHOD##################################

############################################################################
# FirstBest
# @param [graph] Graph
# @param [S] Set of nodes
# @param [Sp] Set of nodes
# @param [cut_v] Neighborhood Size
def firstBest(graph, S,Sp, cut_v):
    """  """
    sample = graph._graph.keys()
    shuffle(sample)

    for node in sample:
        total = cut_value(graph, S, Sp, cut_v, node, True)
        if total > cut_v:
            swap(node,S,Sp)
            return total        
    return cut_v
    