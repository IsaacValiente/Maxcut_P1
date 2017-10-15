#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Graph
import sys

##############################################
# MAIN

def pprint(g):
    print("{'", end="")
    first = True
    for node in g:
        if first:
            first = False
            print (node+"': {", end="")
        else:
            print ("  "+node+"': {", end="")
        for y in g[node]:
            print ("'"+y+"'",end="")

        print("}")
    print("}")

def main(argv):
    connections = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'D'), ('E', 'F'), ('F', 'C')]

    g = Graph(connections)

    pprint(g._graph)

if __name__ == "__main__":
    main(sys.argv)