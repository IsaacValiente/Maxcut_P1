import copy
from random import randint

###################################################################
# generate_initial
# @param [graph] Graph
# @param [random] Boolean : Use random generation
def generate_initial(graph, random=False):
    """ Generate initial solution """
    partitionA = set()
    partitionB = set()
    #RANDOM
    if random:
        for node in graph._graph:
            if randint(0,1) == 0:
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
    return (partitionA,partitionB)

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
  


def cut_value(graph, solution):
    """ Calculate weight of the cut solution """
    
    cutWeight = 0
    partition = solution._partitionA

    for node in partition:
        # print node
        for connection in graph._graph[node]:
            # print connection[0]
            if (connection[0]) not in (partition):
                cutWeight += connection[1]

    return cutWeight

# def solution_improvement() {
    """ Determine better solution algorithm """
# }

def first_best(graph, solution):
    """ Calculate first best of vicinity """

    print('-- first best')
    # max iteration number: vecinity size
    for node in solution._partitionB:
        # print node
        new_solution = copy.deepcopy(solution)
        new_node = solution.choose_random_node('B')
        print('node candidate: ' + str(new_node))
        new_solution.move(new_node)
        value = cut_value(graph, new_solution)
        if (value > solution._value):
            print('better solution found: ' + str(value))
            solution = new_solution
            solution.set_value(value)
            break
    print('--\n')

    print('-- new solution')
    print(solution)
    print('--\n')

def best_best(graph, solution):
    """ Calculate best best of vicinity """
    print('-- best best')
    # iteration number: vecinity size
    for node in solution._partitionB:
        # print node
        new_solution = copy.deepcopy(solution)
        new_node = solution.choose_random_node('B')
        print('node candidate: ' + str(new_node))
        new_solution.move(new_node)
        value = cut_value(graph, new_solution)
        if (value > solution._value):
            print('better solution found: ' + str(value))
            solution = new_solution
            solution.set_value(value)

    print('--\n')

    print('-- new solution')
    print(solution)
    print('--\n')

