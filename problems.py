import abc
from collections import deque

class Problem(metaclass=abc.ABCMeta):
    initialState = None

    def __init__(self, initialState):
        self.initialState = initialState

    @abc.abstractmethod
    def _calculateCost(self, fromState, toState):
        raise NotImplementedError

    @abc.abstractmethod
    # Return the successors of a given state
    def expand(selfs, state):
        raise NotImplementedError

    # Return the successors with a cost for each successor (operator)
    def expandWithCosts(self, state, costComputer=None):
        successors = self.expand(state)

        if costComputer is None:
            for s in successors:
                yield s, self._calculateCost(state, s)
        else:
            for s in successors:
                yield s, costComputer.compute(state, s)

    @abc.abstractmethod
    def isGoal(self, state):
        raise NotImplementedError

from states import MapState

class MapProblem(Problem):
    target = None
    _roads = None
    def __init__(self, roads, source, target):
        self._roads = roads
        I = MapState(source, roads[source].coordinates)
        super().__init__(I)

        self.target = MapState(target, roads[target].coordinates)

    def __hash__(self):
        return hash((self.initialState, self.target))

    def __eq__(self, other):
        return (self.initialState, self.target) == (other.initialState, other.target)

    def _calculateCost(self, fromState, toState):
        for l in self._roads[fromState.junctionIdx].links:
            if l.target == toState.junctionIdx:
                return l.distance

        raise ValueError

    def expand(self, state):
        for l in self._roads[state.junctionIdx].links:
            yield MapState(l.target, self._roads[l.target].coordinates)

    def isGoal(self, state):
        return state.junctionIdx == self.target.junctionIdx

from states import BusState
from astar import AStar
from heuristics import L2DistanceHeuristic

class BusProblem(Problem):
    orders = None
    def __init__(self, startingPoint:int, orders:list):
        self.orders = orders
        self._astar = AStar(L2DistanceHeuristic(), shouldCache = True)
        I = BusState(startingPoint, self.orders.copy(), [], [])
        super().__init__(I)

    def isGoal(self, state):
        return state.isGoal()

    def _calculateCost(self, fromState, toState):
        raise NotImplementedError

    # Return all the successors of a given state
    def expand(self, state):
        for order in state.waitingOrders:
            yield self._getNewStateAtLoc(state, order[0])

        for order in state.ordersOnBus:
            yield self._getNewStateAtLoc(state, order[1])

    # Get the new state created after going from one state to a new location (on map)
    def _getNewStateAtLoc(self, previousState : BusState, newLoc : int):

        newWaiting = deque()
        newOnBus = deque()
        newFinished = deque(previousState.finishedOrders.copy())

        for order in previousState.waitingOrders :
            if order[0] == newLoc :
                newOnBus.append(order)
            else :
                newWaiting.append(order)

        for order in previousState.ordersOnBus :
            if order[1] == newLoc :
                newFinished.append(order)
            else :
                newOnBus.append(order)

        return BusState(newLoc, newWaiting, newOnBus, newFinished)

    @staticmethod
    def load(filepath):
        with open(filepath, "r") as f:
            startingPoint = int(f.readline())
            ordersNum = int(f.readline())

            orders = [None] * ordersNum

            for i in range(ordersNum):
                order = f.readline().split("\t")
                orders[i] = (int(order[0]), int(order[1]))

        return BusProblem(startingPoint, orders)