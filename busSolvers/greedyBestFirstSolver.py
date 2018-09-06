from . import GreedySolver
import numpy as np

class GreedyBestFirstSolver(GreedySolver):
    def __init__(self, roads, astar, scorer):
        super().__init__(roads, astar, scorer)

    # Find the next state to develop
    # returns the state with the minimal score to reach
    def _getNextState(self, problem, currState):
        return min(problem.expand(currState),
                        key=lambda state: self._scorer.compute(currState, state))
