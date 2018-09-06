from heuristics import Heuristic
from ways import compute_distance


class TSPCustomHeuristic(Heuristic) :
    _distMat = None
    _junctionToMatIdx = None

    def __init__(self, roads, initialState) :
        self.roads = roads
        super().__init__()

    # Estimate heuristically the minimal cost from the given state to the problem's goal
    def estimate(self, problem, state) :
        return max(state.waitingOrders,
                   lambda w : compute_distance
                   (self.roads[state.junctionIdx].coordinates,
                    self.roads[w[0]].coordinates))


