import random

class Solution():
    """ Solution data structure """

    def __init__(self, partitionA, partitionB, cutWeight):
        self._partitionA = partitionA
        self._partitionB = partitionB
        self._value = cutWeight

    def set_value(self, cutWeight):
        self._value = cutWeight

    def add(self, node):
        partition = self._partitionA
 
        if node in partition:
            return
        partition.add(node)

    def move(self, node):
        partitionA = self._partitionA
        partitionB = self._partitionB

        # print partitionB

        # remove node from partition B
        partitionB.remove(node)

        # add node to partition A
        self.add(node)

    def choose_random_node(self, partitionName):
        if partitionName == 'A':
            partition = self._partitionA
        if partitionName == 'B':
            partition = self._partitionB

        if not partition: 
          return
        return random.sample(partition, 1)[0]

    def __str__(self):
        return 'partitionA: ' + str(self._partitionA) + '\npartitionB: ' + str(self._partitionB) + '\nvalue: ' + str(self._value)