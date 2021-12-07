#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
	def __init__(self, gui_view):
		self._scenario = None

	def setupWithScenario(self, scenario):
		self._scenario = scenario

	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	def defaultRandomTour(self, time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time() - start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation(ncities)
			route = []
			# Now build the route using the random permutation
			for i in range(ncities):
				route.append(cities[perm[i]])
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	class Node:
		def __init__(self, index, degree):
			self.cityIndex = index
			self.degree = degree

		def updateDegree(self, newDegree):
			degree = newDegree

	class EdgeVal:
		def __init__(self, node1, node2, cost):
			self.node1 = node1
			self.node2 = node2
			self.cost = cost

	def greedy(self, time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		start_time = time.time()
		sortedEdges = []
		for i in range(ncities):
			for j in range(i + 1, ncities):
				cost = cities[i].costTo(cities[j])
				if cost == math.inf:
					continue
				node1 = self.Node(i, 0)
				node2 = self.Node(j, 0)
				newEdge = self.EdgeVal(node1, node2, cost)
				sortedEdges.append(newEdge)
		sortedEdges.sort(key=lambda x: x.cost)
		edgeRoute = []
		visited = set()
		for edgeIndex in range(len(sortedEdges)):
			if len(edgeRoute) == ncities:
				break

			if (not (sortedEdges[edgeIndex].node2.cityIndex in visited)) or (sortedEdges[edgeIndex].node1.degree < 2 and sortedEdges[edgeIndex].node2.degree < 2 and len(edgeRoute) == ncities - 1):
				self.updateDegree(sortedEdges, sortedEdges[edgeIndex].node1.cityIndex)
				self.updateDegree(sortedEdges, sortedEdges[edgeIndex].node2.cityIndex)
				visited.add(sortedEdges[edgeIndex].node2.cityIndex)
				edgeRoute.append(sortedEdges[edgeIndex])
		route = []
		for i in range(len(edgeRoute) - 1, -1, -1):
			if i == 0:
				route.append(cities[edgeRoute[i].node1.cityIndex])
				route.append(cities[edgeRoute[i].node2.cityIndex])
			else:
				route.append(cities[edgeRoute[i].node2.cityIndex])
		end_time = time.time()
		bssf = TSPSolution(route)
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = 1
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	def updateDegree(self, list, cityIndex):
		for i in range(len(list)):
			if list[i].node1.cityIndex == cityIndex:
				list[i].node1.degree += 1
			elif list[i].node2.cityIndex == cityIndex:
				list[i].node2.degree += 1

	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''

	def branchAndBound(self, time_allowance=60.0):
		pass

	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

	def fancy(self, time_allowance=60.0):
		pass
