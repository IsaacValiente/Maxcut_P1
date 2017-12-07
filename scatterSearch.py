#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import pow
from random import randint

from graph import Graph
from solution import Solution
from ssMethods import diversification, improvement, combination, generateSubSet, getMinRS, getMax


###################################################################
# scatterSearch
# @param [graph] Graph
# @param [alpha] Value used in diversification
# @param [b] Size of refSet
def scatterSearch(graph, alpha, b):
	""" Scatter search metaheuristic for MaxCut"""

	#Generate P
	P = []
	refSet = []
	refSet_pos = []
	c = 0
	powb2 = pow(b,2)
	while c < powb2:
		x = diversification(graph, alpha)
		S,Sp,cut_V = improvement(graph, x)
		if (not (S,Sp,cut_V) in P) and (not (Sp,S,cut_V) in P):
			P.append((S,Sp,cut_V))
			c = c + 1

			#Build RefSet
			if len(refSet) < b/2:
				refSet.append((S,Sp,cut_V))
				refSet_pos.append(c)
				if len(refSet) == b/2:
					#Get new min
					minrefSet, minrefSet_pos = getMinRS(refSet, b/2)

			elif cut_V > minrefSet:
				refSet[minrefSet_pos] = (S,Sp,cut_V)
				refSet_pos[minrefSet_pos] = c

				#Get new min
				minrefSet, minrefSet_pos = getMinRS(refSet, b/2)

	#Build Diverse RefSet
	pos = randint(0,(c-1))
	for i in range(0,(b/2)):
		while (pos in refSet_pos):
			 pos =randint(0,(c-1))

		refSet.append(P[pos])
		refSet_pos.append(pos)

	#Get new min
	minrefSet, minrefSet_pos = getMinRS(refSet, b)		


	newSolutions = True
	while newSolutions:
		newSolutions = False
		#Generate subset
		newSubSet = generateSubSet(refSet,b)
		for subSet in newSubSet:
			trial_sol = combination(graph, subSet)
			#Improvement
			for sol in trial_sol:
				I,Ip,cut_I = improvement(graph, sol)

				#Update RefSet
				if cut_I > minrefSet:
					if (not (I,Ip,cut_I) in refSet) and (not (Ip,I,cut_I) in refSet):
						refSet[minrefSet_pos] = (I,Ip,cut_I)
						newSolutions = True
						minrefSet, minrefSet_pos = getMinRS(refSet, b)

	return getMax(refSet,b)





