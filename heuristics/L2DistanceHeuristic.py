from . import Heuristic
from costs import L2DistanceCost

# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        return  L2DistanceCost(problem._roads).compute(state, problem.target)

