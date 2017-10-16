import random

class Solution():
    """ Solution data structure """

    def __init__(self, partitionA, partitionB, cutWeight):
        self._partitionA = partitionA
        self._partitionB = partitionB
        self._value = cutWeight

    def set_value(self, cutWeight):
        """ Set value of the solution """
        self._value = cutWeight

    def add(self, node):
        """ Add node to partition A """
        partition = self._partitionA
 
        if node in partition:
            return
        partition.add(node)

    def move(self, node):
        """ Move node from partition B to partition A """
        partitionA = self._partitionA
        partitionB = self._partitionB

        partitionB.remove(node)
        self.add(node)

    def choose_random_node(self, partitionName):
        """ Choose random node from requested partition """
        if partitionName == 'A':
            partition = self._partitionA
        if partitionName == 'B':
            partition = self._partitionB

        if not partition: 
          return
        return random.sample(partition, 1)[0]

    def __str__(self):
        return 'partitionA: ' + str(self._partitionA) + '\npartitionB: ' + str(self._partitionB) + '\nvalue: ' + str(self._value)