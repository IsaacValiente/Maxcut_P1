import copy

def generate_initial(self):
		""" Generate initial solution """

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

    print '-- first best'
    # max iteration number: vecinity size
    for node in solution._partitionB:
        # print node
        new_solution = copy.deepcopy(solution)
        new_node = solution.choose_random_node('B')
        print 'node candidate: ' + str(new_node)
        new_solution.move(new_node)
        value = cut_value(graph, new_solution)
        if (value > solution._value):
            print 'better solution found: ' + str(value)
            solution = new_solution
            solution.set_value(value)
            break
    print '--\n'

    print '-- new solution'
    print solution
    print '--\n'

def best_best(graph, solution):
    """ Calculate best best of vicinity """
    print '-- best best'
    # iteration number: vecinity size
    for node in solution._partitionB:
        # print node
        new_solution = copy.deepcopy(solution)
        new_node = solution.choose_random_node('B')
        print 'node candidate: ' + str(new_node)
        new_solution.move(new_node)
        value = cut_value(graph, new_solution)
        if (value > solution._value):
            print 'better solution found: ' + str(value)
            solution = new_solution
            solution.set_value(value)

    print '--\n'

    print '-- new solution'
    print solution
    print '--\n'

