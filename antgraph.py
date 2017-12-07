from collections import defaultdict
from random import choice, sample

class AntGraph(object):
    """ Graph data structure """

    def __init__(self, connections, tMax):
        # self._graph = defaultdict(set)
        self._graph = defaultdict(list)
        self._tMax = tMax
        self.add_connections(connections)

    def rand_node(self):
        keys = self._graph.keys()
        node = choice(keys)
        return node

    def first(self):
        u_keys = (self._graph.keys())
        s_keys = sorted(u_keys)
        node = s_keys[0] if len(s_keys) > 0 else None
        return node

    def get_sample(self,percentage):
        keys = self._graph.keys()
        k = len(keys) * percentage // 100
        indices = sample(xrange(len(keys)), k)
        p_sample = [keys[i] for i in indices]
        return p_sample     

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2, weight in connections:
            self.add(int(node1), int(node2), int(weight), float(self._tMax))

    def add(self, node1, node2, weight, tMax):
        """ Add connection between node1 and node2 """

        self._graph[node1].append((node2,weight,tMax))
        self._graph[node2].append((node1,weight,tMax))
        # self._graph[node1].add((node2,weight,tMax))
        # self._graph[node2].add((node1,weight,tMax))

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """
        connected = False
        if node1 in self._graph:
            for node,w,t in self._graph[node1]:
                if node2 == node:
                    connected = True
                    break
        return connected

    def weight(self, node1, node2):
        """ Weight of vertex (node1,node2)"""
        weight = 0
        for node,w,t in self._graph[node1]:
            if node2 == node:
                weight = w
                break
        return weight

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))