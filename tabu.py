from numpy import inf
from random import randint, uniform
from graph import Graph
from copy import deepcopy

from local_search import totalCutValue
from solution import Solution

###################################################################
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

###################################################################
# updateTabuList
# @param [tList] Tabu List
def updateTabuList(tList):
    """  """
    tList[:]=[(mov[0],mov[1]-1) for mov in tList if not (mov[1]-1 == 0)]

###################################################################
# updateTabuList
# @param [tList] Tabu List
# @param [node] node
# @param [ttenure] Tabu tenure

def tappend(tList,node,ttenure):
    """  """
    exist = False
    for i,move in enumerate(tList):
        if move[0] == node:
            tList[i] = (node, ttenure)
            exist = True
    if not exist:
        tList.append((node,ttenure))

###################################################################
# movTabu
# @param [node] node
# @param [tList] Tabu List

def movTabu(node,tList):
    """  """
    exist = False
    for move in tList:
        if move[0] == node:
            exist = True
            return exist
    return exist

###################################################################
# movTabu
# @param [node] node
# @param [tList] Tabu List

def tabuTotal(graph, A, B, sum, n1, n2):
    wn1a = 0
    wn1b = 0
    wn2a = 0
    wn2b = 0
    
    #WnB
    connect_n1 = graph._graph[n1]   
    connect_n2 = graph._graph[n2]

    for c1 in connect_n1:
        if c1[0] in A:
            if c1[0] != n2:
                wn1a += c1[1]
        else:
            if c1[0] != n2:
               wn1b += c1[1]

    for c2 in connect_n2:
        if c2[0] in A:
            if c2[0] != n1:
                wn2a += c2[1]
        else:
            if c2[0] != n1:
                wn2b += c2[1]
    if n1 in A:
        wn1 = wn1a - wn1b
    else:
        wn1 = wn1b - wn1a
    if n2 in A:
        wn2 = wn2a - wn2b
    else:
        wn2 = wn2b - wn2a
    return sum+wn1+wn2

###################################################################
# generateNeighborT
# @param [graph] Graph
# @param [s1] Set of nodes
# @param [s2] Set of nodes
# @param [bestcut] Boolean : Use random generation
# @param [neighSize] Neighborhood Size
# @param [tabulist] Tabu list

def generateNeighborT(graph, s1,s2, sum, neighSize, tList, minTIter, maxTIter):
    """  """
    best = -inf
    tot = -inf
    act = graph.first()
    while act < neighSize:
        n1 = graph.rand_node()
        while n1 == act:
            n1 = graph.rand_node()
        tot = tabuTotal(graph,s1,s2, sum, act,n1)
        if tot >= sum:
            tappend(tList,act,randint(minTIter, maxTIter))
            swap(act,s1,s2)
            swap(n1,s1,s2)
            return tot
        elif not movTabu(act,tList) :
            if tot > best :
                node1 = act
                node2 = n1
                best = tot
        act = act + 1

    swap(node1,s1,s2)
    swap(node2,s1,s2)
    tappend(tList,node1,randint(minTIter, maxTIter))
    return best

###################################################################
# tabuSearch
# @param [maxIWoImp] Maximun iterations without improvement
# @param [graph] Graph
# @param [s1] Set of nodes
# @param [s2] Set of nodes
# @param [neighSize] Neighborhood Size
# @param [minTIter] Minimun tabu iterations
# @param [maxTIter] Maximun tabu iterations

def tabuSearch(maxIWoImp, graph, s1, s2, neighSize, minTIter, maxTIter):
    """  Tabu search metaheuristic """
    tList = []
    c = 0
    u1 = deepcopy(s1)
    u2 = deepcopy(s2)
    total = totalCutValue(graph,s1,s2)
    u_total = totalCutValue(graph,u1,u2)
    while c < maxIWoImp :
        total = generateNeighborT(graph, s1, s2, total, neighSize, tList, minTIter, maxTIter)
        if total > u_total:
            u1 = deepcopy(s1)
            u2 = deepcopy(s2)
            u_total = total
            print("Iteraciones antes de mejorar: "+str(c))
            c = 0
            print(u_total)

        else:
            c = c + 1
        updateTabuList(tList)
    sol = Solution(u1, u2, u_total)
    return sol

###################################################################
# generateNeighborSA
# @param [graph] Graph
# @param [s1] Set of nodes
# @param [s2] Set of nodes
# @param [bestcut] Boolean : Use random generation
# @param [neighSize] Neighborhood Size
# @param [tabulist] Tabu list

def generateNeighborSA(graph, s1,s2, sum, neighSize):
    """  """
    best = -inf
    act = 1
    while act < neighSize :
        swap(act,s1,s2)
        n1 = graph.rand_node()
        swap(n1,s1,s2)

        # value of the new cut
        cut = totalCutValue(graph,s1,s2)

        if cut >= sum:
            best = cut
            break
        elif cut > best :
            node1 = act
            node2 = n1
            best = cut
        swap(act,s1,s2)
        swap(n1,s1,s2)
        act = act + 1
    if act == neighSize:
        swap(node1,s1,s2)
        swap(node2,s1,s2)
    return s1,s2

###################################################################
# Annealing
# @param [maxIWoImp] Maximun iterations without improvement
# @param [graph] Graph
# @param [s1] Set of nodes
# @param [s2] Set of nodes
# @param [k] Boolean : Use random generation
# @param [a] Neighborhood Size
# @param [temp] Maximun tabu size
# @param [sum] Minimun tabu iterations
# @param [neighSize] Maximun tabu iterations

def annealing(maxIWoImp, graph, s1, s2, K, A, temp, initCut, neighSize ):
    """ Simulated Annealing metaheuristic"""
    c,k,a, = 0,0,0
    u1,u2 = s1,s2

    # how to set alpha and beta?
    alpha = 0.7
    beta = 1.1

    while c < maxIWoImp :
        print("c: "+c+'\n')
        startingCut = totalCutValue(graph, s1, s2)

        startingSum = startingCut
        print("starting sum: "+str(startingSum)+'\n')        

        while k < K and a < A:
            t1,t2 = s1,s2
            s1,s2 = generateNeighborSA(graph, s1, s2, startingCut, neighSize)

            print("new neighbour: "+str(s1)+'\n'+str(s1)+'\n')

            prevCut = totalCutValue(graph, t1, t2)
            newCut = totalCutValue(graph, s1, s2)

            print("new cut: "+str(totalCutValue(graph, s1, s2))+'\n')            

            if newCut > startingCut:
                if newCut > initCut:
                    u1,u2 = s1,s2
                a = a + 1
            else:
                delta = uniform(0, 1)
                if delta > ((newCut - prevCut)/temp):
                    s1,s2 = t1,t2
                    a = a + 1
            k = k + 1

        temp = alpha*temp
        K = beta*K
        k,a = 0,0

        print('temp: '+temp)
        print('K: '+K)
        print('A:'+A)

        endingCut = totalCutValue(graph, s1, s2)
        if endingCut <= startingSum:
            c = c + 1
        else:
            c = 0 

    return u1,u2
