from __future__ import division
from copy import deepcopy, copy
from random import randint
from numpy import random, inf
from collections import defaultdict
from graph import Graph
from solution import Solution
from local_search import weight, totalCutValue
from tabu_sa import swap, calculateMovement


###################################################################
# switch_vertex
# @param [vertex]
# @param [cutVectors]
def switch_vertex(vertex, cutVectors):
    """ Switch given vertex's cut vector """

    cutVectors[vertex] = (-1) * cutVectors[vertex]


###################################################################
# update_deltas
# @param [graph]
# @param [vertex]
# @param [cutVectors]
# @param [deltaFs]
# @param [alpha]
# @param [beta]

def update_deltas(graph, vertex, cutVectors, deltaFs, alpha, beta):
    """ Update delta value for vertices given """

    # adjust delta value for chosen vertex
    deltaFs[vertex] = (-1) * deltaFs[vertex]

    # updated vertices list for later candidate set update
    updatedVertices = [vertex]

    for edge in graph._graph[vertex]:
        connection = edge[0]
        weight = edge[1]
        pheromone = edge[2]

        calc = 2 * cutVectors[vertex] * cutVectors[connection] * pow(pheromone, alpha) * pow(weight, beta) 
        deltaFs[connection] = deltaFs[connection] + calc
        updatedVertices.append(connection)
    
    return updatedVertices


###################################################################
# calc_deltas
# @param [graph]
# @param [cutVectors]
# @param [deltaFs]
# @param [beta]

def calc_deltas(graph, cutVectors, deltaFs, alpha, beta):
    """ Calculate delta value for each vertex """

    # candidate set
    candidateSet = set()

    for vertex in graph._graph:
        deltaFi = 0
        for edge in graph._graph[vertex]:
            connection = edge[0]
            weight = edge[1]
            pheromone = edge[2]

            incValue = cutVectors[vertex] * cutVectors[connection] * pow(pheromone, alpha) * pow(weight, beta) 
            deltaFs[vertex] = deltaFs[vertex] + incValue

        if deltaFs[vertex] > 0:
            candidateSet.add(vertex)

    return candidateSet

###################################################################
# update_prob
# @param [vertexNum]
# @param [deltaFs]
# @param [candidateSet]
# @param [vertexProbs]

def update_probs(vertexNum, deltaFs, candidateSet, vertexProbs):
    """ Update choose probability for all vertices """

    sum = 0
    candidateDeltas = 0
    for candidate in candidateSet:
        candidateDeltas = candidateDeltas + deltaFs[candidate]

    i = 1
    while i <= vertexNum:
        vertexProb = deltaFs[i] / candidateDeltas

        if vertexProb < 0:
            vertexProbs[i] = 0
        else:
            vertexProbs[i] = vertexProb

        sum = sum + vertexProbs[i]
        i = i + 1


###################################################################
# update_candidates
# @param [updatedVertices]
# @param [deltaFs]
# @param [candidateSet]

def update_candidates(updatedVertices, deltaFs, candidateSet):
    """ Update candidate set according to updated deltas """

    for vertex in updatedVertices:
        if deltaFs[vertex] <= 0:
            if vertex in candidateSet:
                candidateSet.remove(vertex) 
        else:
            candidateSet.add(vertex) 


###################################################################
# local_search
# @param [graph]
# @param [vertexNum]
# @param [solution]

def local_search(graph, vertexNum, solution):
    """ Local search strategy """

    cutVectors = solution[0]
    partitionA = solution[1]
    partitionB = solution[2]
    cut = solution[3]

    vertex = 1
    while vertex <= vertexNum:
        deltaL = 0
        for edge in graph._graph[vertex]:
            connection = edge[0]
            weight = edge[1]
            calc = cutVectors[vertex] * cutVectors[connection] * weight
            deltaL = deltaL + calc
        
        if deltaL > 0:
            switch_vertex(vertex, cutVectors)
            cut = calculateMovement(graph, partitionA, partitionB, cut, [vertex])
            swap(vertex, partitionA, partitionB)
            # start over from to vertex 1
            vertex = 1
        else: 
            vertex = vertex + 1

    newSolution = (cutVectors, partitionA, partitionB, cut)
    return newSolution


###################################################################
# update_pheromone
# @param [graph]
# @param [solutions]
# @param [it]
# @param [p]
# @param [Q]
# @param [best]
# @param [better]
def update_pheromone(graph, solutions, it, p, Q, best, better):
    """ Global pheromone update """

    for vertex in graph._graph:
        for i, edge in enumerate(graph._graph[vertex]):
            connection = edge[0]
            isCut = False

            for sol in solutions:
                cutVectors = sol[0]
                if cutVectors[vertex] != cutVectors[connection]:
                    isCut = True
                    break
            if isCut:
                den = Q + best - better
                # hack to avoid division by zero
                if den == 0:
                    den = den - 1
                deltaP = 1 / den 
            else:
                deltaP = 0

            calc = (1 - p) * edge[2] + deltaP
            graph._graph[vertex][i] = (edge[0], edge[1], calc)

    # check print of p constant
    # print('p: ' + str(p))


###################################################################
# print_pheromone
# @param [graph]

def print_pheromone(graph):
    """  """

    print 'pheromone list'
    for vertex in graph._graph:
        for edge in graph._graph[vertex]:
            print edge[2],

###################################################################
# ant_cut
# @param [graph]
# @param [vertexNum]
# @param [itNum]
# @param [antNum]
# @param [alpha]
# @param [beta]

def ant_cut(graph, vertexNum, itNum, antNum, alpha, beta):
    """ Ant cut """

    # initiate cut vectors, deltas, vertex probabilities and candidate set
    cutVectors = [1] * (vertexNum + 1)
    deltaFs = [0] * (vertexNum + 1)
    vertexProbs = [0] * (vertexNum + 1)

    # solutions structure
    solutions = []
    better = ([], set(), set(), -inf)

    # calculate initial delta values and candidate set
    candidateSet = calc_deltas(graph, cutVectors, deltaFs, alpha, beta)

    initDeltas = copy(deltaFs)
    initCandidates = copy(candidateSet)
    initProbs = copy(vertexProbs)

    i = 0
    while i < itNum:
        # check print for iteration number
        # print('vuelta: ' + str(i))
        antCount = 0
        while antCount < antNum:
            # reset cut vectors, candidate set, delta and probabilities
            cutVectors = [1] * (vertexNum + 1)
            candidateSet = copy(initCandidates)
            vertexProbs = copy(initProbs)
            deltaFs = copy(initDeltas)

            partitionA = set(range(vertexNum + 1))
            partitionB = set()
            cutValue = 0

            while candidateSet:
                # update probabilities for each vertex
                update_probs(vertexNum, deltaFs, candidateSet, vertexProbs)
                
                # choose vertex from probabilities array
                choice = random.choice(vertexNum + 1, 1, p=vertexProbs)
                vertex = choice[0]

                # update cut vector, deltaFs and candidate set
                cutVectors[vertex] = (-1) * cutVectors[vertex]
                updatedVertices = update_deltas(graph, vertex, cutVectors, deltaFs, alpha, beta)

                update_candidates(updatedVertices, deltaFs, candidateSet)

                # update partitions and calculate cut value
                cutValue = calculateMovement(graph, partitionA, partitionB, cutValue, [vertex])
                swap(vertex, partitionA, partitionB)

            # store ant solution
            if not cutVectors in solutions:
                solutions.append((cutVectors, partitionA, partitionB, cutValue))

            antCount = antCount + 1

        # local search optimization for each solution
        best = ([], set(), set(), -inf)
        for sol in solutions:
            # check print to observe how the algorithm behaves
            # print sol[3]
            if sol[3] > 0:
                newSolution = local_search(graph, vertexNum, sol)
                cutValue = newSolution[3]
                if cutValue > best[3]:
                    best = copy(newSolution)
                    if cutValue > better[3]:
                        better = copy(newSolution)

            # algorithm efficiency decays to zero, return
            else:
                # results print
                print('\nsolution: \n(<cut vectors>, <partition A>, <partition B>, <cut value>)')
                print better
                print('\nmax iteration number: ' + str(itNum))
                print('number of ants: ' + str(antNum))
                print('p factor: ' + str(p))
                return

        # check print 
        # print better[3]

        # global pheromone update
        solutions.append(better)

        Q = 100
        # different p values used
        p = 0.00009
        #p = 0.005
        # p = 0.00002
        # p = 0.009
        update_pheromone(graph, solutions, i, p, Q, best[3], better[3])

        # solutions list reset
        solutions = []

        i = i + 1

    # solution print
    print('\nsolution: \n(<cut vectors>, <partition A>, <partition B>, <cut value>)')
    print better
    print('\nmax iteration number: ' + str(itNum))
    print('number of ants: ' + str(antNum))
    print('p factor: ' + str(p))
