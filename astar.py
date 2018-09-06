import numpy as np
import sys
from heapDict import heapdict
from states import State

class AStar :
    cost = None
    heuristic = None
    _cache = None
    shouldCache = None

    def __init__(self, heuristic, cost = None, shouldCache = False) :
        self.heuristic = heuristic
        self.shouldCache = shouldCache
        self.cost = cost

        # Handles the cache. No reason to change this code.
        if self.shouldCache :
            self._cache = { }

    # Get's from the cache. No reason to change this code.
    def _getFromCache(self, problem) :
        if self.shouldCache :
            return self._cache.get(problem)

        return None

    # Get's from the cache. No reason to change this code.
    def _storeInCache(self, problem, value) :
        if not self.shouldCache :
            return

        self._cache[problem] = value

    # Run A*
    def run(self, problem):
        # Check if we already have this problem in the cache.
        # No reason to change this code.
        source = problem.initialState
        if self.shouldCache:
            res = self._getFromCache(problem)

            if res is not None:
                return res

        parents = {source: None}
        g_score = {source: 0}
        open_set = heapdict()
        open_set[source] = self.heuristic.estimate(problem, source)
        developed = 0
        value = [], -1, -1, developed

        while open_set:
            current_state, cost = open_set.popitem()

            if problem.isGoal(current_state):
                value = self._reconstructPath(parents, current_state), \
                        cost, \
                        self.heuristic.estimate(problem, problem.initialState), \
                        developed
                break

            developed += 1
            for s in problem.expandWithCosts(current_state, self.cost):
                new_g_score = g_score[current_state] + s[1]
                next_state = s[0]

                if next_state not in g_score or new_g_score < g_score[next_state]:
                    g_score[next_state] = new_g_score
                    parents[next_state] = current_state
                    open_set[next_state] = new_g_score + self.heuristic.estimate(problem, next_state)

        self._storeInCache(problem, value)
        return value

    # Reconstruct the path from a given goal by its parent and so on
    def _reconstructPath(self, parents, goal):
        def generatePath():
            curr = goal
            while curr:
                yield curr
                curr = parents[curr]

        return list(reversed(list(generatePath())))
