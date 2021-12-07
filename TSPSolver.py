#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
# elif PYQT_VER == 'PYQT4':
#     from PyQt4.QtCore import QLineF, QPointF
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

    def greedy(self, time_allowance=60.0):
        cities = self._scenario.getCities()
        foundTour = False
        count = 0
        bssf = None
        results = {}
        start_time = time.time()
        route = []
        while not foundTour and time.time() - start_time < time_allowance:
            visited = set()
            current_city = cities[count]
            route.clear()
            route.append(cities[count])
            while len(visited) < len(cities):
                visited.add(current_city)
                max_city = None
                max_cost = 0
                for testCity in cities:
                    if testCity not in visited:
                        if max_cost < current_city.costTo(testCity) < math.inf:
                            max_cost = current_city.costTo(testCity)
                            max_city = testCity

                if max_city is None:
                    break

                route.append(max_city)
                current_city = max_city

            count += 1
            route_cost = TSPSolution(route).cost
            if len(visited) == len(cities) and route_cost < math.inf:
                if bssf is None:
                    bssf = TSPSolution(route)
                elif route_cost < bssf.cost:
                    bssf = TSPSolution(route)

            if count == len(cities):
                foundTour = True

        end_time = time.time()
        results['cost'] = bssf.cost
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = 0
        results['total'] = None
        results['pruned'] = None
        return results

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
        cities = self._scenario.getCities()
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()

        route = []
        while not foundTour and time.time() - start_time < time_allowance:
            visited = set()
            current_city = cities[count]
            route.clear()
            route.append(cities[count])
            while len(visited) < len(cities):
                visited.add(current_city)
                min_city = None
                min_cost = math.inf
                for testCity in cities:
                    if testCity not in visited:
                        if current_city.costTo(testCity) < min_cost:
                            min_cost = current_city.costTo(testCity)
                            min_city = testCity

                if min_city is None:
                    break

                route.append(min_city)
                current_city = min_city

            count += 1
            route_cost = TSPSolution(route).cost
            if len(visited) == len(cities) and route_cost < math.inf:
                if bssf is None:
                    bssf = TSPSolution(route)
                elif route_cost < bssf.cost:
                    bssf = TSPSolution(route)

            if count == len(cities):
                foundTour = True

        end_time = time.time()
        return self.createResults(bssf, start_time, end_time, count, foundTour, 0)

    @staticmethod
    def createResults(bssf, start_time, end_time, count, foundTour, max_queue_size, total=None, pruned=None):
        return {'cost': bssf.cost if foundTour else math.inf, 'time': end_time - start_time, 'count': count,
                'soln': bssf, 'max': max_queue_size, 'total': total, 'pruned': pruned}
