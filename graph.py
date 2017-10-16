from collections import defaultdict


class Graph(object):
    """ Graph data structure """

    def __init__(self, connections):
        self._graph = defaultdict(set)
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2, weight in connections:
            self.add(node1, node2, weight)

    def add(self, node1, node2, weight):
        """ Add connection between node1 and node2 """

        self._graph[node1].add((node2,weight))
        self._graph[node2].add((node1,weight))

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """
        connected = False
        if node1 in self._graph:
            for node,w in self._graph[node1]:
                if node2 == node:
                    connected = True
                    break
        return connected

    def weight(self, node1, node2):
        """ Is node1 directly connected to node2 """
        weight = 0
        for node,w in self._graph[node1]:
            if node2 == node:
                weight = w
                break
        return weight

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))