#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy import inf
from copy import deepcopy
from random import shuffle, randint, sample

from graph import Graph
from solution import Solution

############################################################################

############################FUNCTIONS#######################################

############################################################################
# totalCutValue
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
# swap
# @param [node] node to swap
# @param [s1] Partition1
# @param [s2] Partition2
def swap(node,s1,s2):
    """ Swap partition of node"""
    if node in s1:
        s1.remove(node)
        s2.add(node) 
    else:
        s2.remove(node)
        s1.add(node)

############################################################################

######################DIVERSIFICATION METHOD################################

############################################################################
# diffSigmas : Calculate the difference between sigma and sigmap
# @param [graph] Graph
# @param [random] Boolean : Use random generation
def minDiff(diff):
    min_v = inf

    for d in diff:
        if d[1] < 0:
            return 0
        
        if d[1] < min_v:
            min_v = d[1]

    return min_v

############################################################################
# diffSigmas : Calculate the difference between sigma and sigmap
# @param [graph] Graph
# @param [random] Boolean : Use random generation
def maxDiff(diff):
    max_v = -inf

    for d in diff:
        if d[1] > max_v:
            max_v = d[1]
    
    if max_v < 0:
        return 0
    
    return max_v  
      
############################################################################
# diffSigmas : Calculate the difference between sigma and sigmap
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
# diffSigmas : Calculate the difference between sigma and sigmap
# @param [graph] Graph
# @param [node] Graph
# @param [S] Graph
# @param [Sp] Graph
def diffSigmas(graph, node, S, Sp):
    sumSigma = 0
    sumSigmaP = 0

    connect_n = graph._graph[node]

    for c in connect_n:
        if c[0] in S:
            sumSigma += c[1]
        else:
            sumSigmaP += c[1]

    return sumSigmaP - sumSigma

############################################################################
# Diversification Generation method C2
# @param [graph] Graph
# @param [random] Boolean : Use random generation
def diversification(graph, alpha):

    #Initialize
    nodes = (graph._graph.keys())
    S = set()
    Sp = set(nodes)
    cut_v = 0
    new_solution = True
    while (new_solution):
        diff = set()
        new_solution = False
        for node in Sp:
            diff.add( (node, diffSigmas(graph, node, S, Sp)) )

        minD = minDiff(diff)
        maxD = maxDiff(diff)
        th = minD + alpha*(maxD-minD)
        if th == 0 :
            return Solution(S,Sp,cut_v)

        Rcl = set()
        for d in diff:
            if d[1] > th:
                Rcl.add(d[0])
        if len(Rcl) > 0:
            new_solution = True
            node = sample(Rcl, 1)[0]
            Sp.remove(node)
            S.add(node)
            oldCut_v = cut_v
            cut_v = cut_value(graph, S, Sp, cut_v, node, False)

    return Solution(S,Sp,cut_v)

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
    act = graph.first()
    sample = graph._graph.keys()
    shuffle(sample)

    for node in sample:
        total = cut_value(graph, S, Sp, cut_v, node, True)
        if total > cut_v:
            swap(node,S,Sp)
            return total        
    return cut_v


############################################################################
# Improvement method
# @param [graph] Graph
# @param [S] Set of nodes
# @param [Sp] Set of nodes
# @param [cut_v] Neighborhood Size

def improvement(graph, solution):
    """  Improvement method using first best"""
    u = deepcopy(solution._partitionA)
    up = deepcopy(solution._partitionB)
    cut_v = solution._value
    oldcut_v = 0
    while cut_v - oldcut_v > 0:
        oldcut_v = cut_v
        cut_v = firstBest(graph, u, up, cut_v)

    return u, up, cut_v



############################################################################

########################COMBINATION METHOD##################################

############################################################################
# sigmas : 
# @param [graph] Graph
# @param [node] Graph
# @param [S] Graph
# @param [Sp] Graph
def sigmas(graph, node, S, Sp):
    sumSigma = 0
    sumSigmaP = 0

    connect_n = graph._graph[node]

    for c in connect_n:
        if c[0] in S:
            sumSigma += c[1]
        elif c[0] in Sp:
            sumSigmaP += c[1]

    return sumSigma, sumSigmaP

############################################################################
# Combination method
# @param [graph] Graph
# @param [subSet] set containing two solutions

def combination(graph, subSet):
    """  Combination method CB2"""
    S1 = subSet[0][0]
    Sp1 = subSet[0][1]
    S2 = subSet[1][0]
    Sp2 = subSet[1][1]

    #Intersection of both solutions
    U = S1 & S2
    Up = Sp1 & Sp2
    cut_v = totalCutValue(graph, U, Up)
    U2 = deepcopy(U)
    Up2 = deepcopy(Up)
    cut_v2 = cut_v

    #Unselected nodes
    nodes = set(graph._graph.keys())
    nodes = nodes - U
    nodes = nodes - Up

    for node in nodes:
        #Quality Solution
        sigma,sigmap = sigmas(graph, node, U, Up)
        if sigma > sigmap:
            Up.add(node)
            cut_v = cut_v + sigma

        else:
            U.add(node)
            cut_v = cut_v + sigmap
            
        #Diversity Solution
        sigma,sigmap = sigmas(graph, node, U2, Up2)
        if randint(0,1) == 0:
            Up2.add(node)
            cut_v2 = cut_v2 + sigma
            
        else:
            U2.add(node)
            cut_v2 = cut_v2 + sigmap

    return [Solution(U2,Up2,cut_v2),Solution(U,Up,cut_v)]

############################################################################

##########################GENERATE SUBSET###################################

############################################################################
# Generate SubSet
# @param [refSet] Graph

def generateSubSet(refSet, b):
    """  Generate SubSet """
    subSet = []
    k = 1
    for i in range(0,b):
        for j in range(k,b):
            subSet.append( (refSet[i], refSet[j]) )
        k = k +1
    return subSet


############################################################################

############################## REFSET ######################################

############################################################################
# getMinRS
# @param [refSet] Graph
# @param [imp_sol] Set of nodes

def getMinRS(refSet, b):  
    """  Position and value of min value"""          
    minrefSet = inf
    for i in range(0,b):
        if refSet[i][2] < minrefSet:
            minrefSet = refSet[i][2]
            minrefSet_pos = i
    return minrefSet, minrefSet_pos

############################################################################
# getMaxRS
# @param [refSet] Graph
# @param [imp_sol] Set of nodes

def getMax(refSet, b):  
    """  Return best solution in refSet"""          
    value = -inf
    for i in range(0,b):
        if refSet[i][2] > value:
            value = refSet[i][2]
            pos = i

    return Solution(refSet[pos][0], refSet[pos][1], refSet[pos][2])


