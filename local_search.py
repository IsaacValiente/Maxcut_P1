import copy, random, math

def generate_initial(self):
	""" Generate initial solution """

def cut_value(graph, solution, candidate):
    """ Calculate weight of the cut solution """
    
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

def first_best(graph, solution, iterations):
    """ Calculate first best of vicinity """
    """ returns True if the solution improved, False otherwise""" 

    improved = False
    iterationsLeft = iterations
    partitionB = copy.deepcopy(solution._partitionB)

    print '-- first best'
    # max iteration number: iterations allowed 
    while iterations > 0 and partitionB:
        candidate = random.sample(partitionB, 1)[0]
        print 'node candidate: ' + str(candidate)
        value = cut_value(graph, solution, candidate)
        if (value > solution._value):
            improved = True
            print 'first best found: ' + str(value)
            solution.move(candidate)
            solution.set_value(value)
            print '-- new solution'
            print solution
            print '--\n'
            # reset left iteration number and update candidate pool
            iterationsLeft = iterations
            partitionB = copy.deepcopy(solution._partitionB)
        else:
            iterationsLeft -= 1
            partitionB.remove(candidate)

    print '--\n'
    print 'got stuck! Could not find a better solution than:'
    return improved

def best_best(graph, solution):
    """ Calculate best best of vicinity """
    """ returns True if the solution improved, False otherwise """ 

    improved = False
    partitionB = copy.deepcopy(solution._partitionB)

    print '-- best best'
    # iteration number: partitionB length
    for candidate in partitionB:
        print 'node candidate: ' + str(candidate)
        value = cut_value(graph, solution, candidate)
        if (value > solution._value):
            improved = True
            print 'better solution found: ' + str(value)
            solution.move(candidate)
            solution.set_value(value)
            print '-- new solution'
            print solution
            print '--\n'   

    print '--\n'
    print 'got stuck! Could not find a better solution than:'    
    return improved

def percentage_best(graph, solution, percentage):
    """ Calculate best best of vicinity percentage """
    """ returns True if the solution improved, False otherwise """ 

    improved = False
    partitionB = copy.deepcopy(solution._partitionB)
    iterations = int(math.floor(len(partitionB) * percentage))

    print '-- ' + str(int(percentage*100)) + '% percentage best (' + str(iterations) + ' iterations)'
    
    # iteration number: percentage over partitionB length
    while iterations > 0:
        candidate = random.sample(partitionB, 1)[0]
        print 'node candidate: ' + str(candidate)
        value = cut_value(graph, solution, candidate)
        if (value > solution._value):
            improved = True
            print 'better solution found: ' + str(value)
            solution.move(candidate)
            solution.set_value(value)
            print '-- new solution'
            print solution
            # calculate new iteration number and update candidate pool
            iterations = int(math.floor(len(solution._partitionB) * percentage))
            partitionB = copy.deepcopy(solution._partitionB)
            print partitionB
            print str(iterations) + ' iterations'
            print '--\n'    

        else:
            iterations -= 1
            partitionB.remove(candidate)

    print '--\n'
    print 'got stuck! Could not find a better solution than:'    
    return improved