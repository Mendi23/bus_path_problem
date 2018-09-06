import numpy as np
from scipy import stats

from astar import AStar
from busSolvers import GreedyBestFirstSolver, GreedyStochasticSolver
from consts import Consts
from costs import L2DistanceCost
from heuristics import L2DistanceHeuristic
from problems import BusProblem
from ways import load_map_from_csv
from itertools import accumulate

REPEATS = 150

# Load the files
roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
prob = BusProblem.load(Consts.getDataFilePath("HAIFA_100.in"))

mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

scorer = L2DistanceCost(roads)

# Run the greedy solver
pickingPath = GreedyBestFirstSolver(roads, mapAstar, scorer).solve(prob)
greedyDistance = pickingPath.getDistance() / 1000
print("Greedy solution: {:.2f}km".format(greedyDistance))

# Run the stochastic solver #REPATS times
solver = GreedyStochasticSolver(roads, mapAstar, scorer,
                                Consts.STOCH_INITIAL_TEMPERATURE,
                                Consts.STOCH_TEMPERATURE_DECAY_FUNCTION,
                                Consts.STOCH_TOP_SCORES_TO_CONSIDER)

results = np.zeros((REPEATS,))

print("Stochastic repeats:")

for i in range(REPEATS):
    print("{}..".format(i+1), end=" ", flush=True)
    results[i] = solver.solve(prob).getDistance() / 1000

bestResult = list(accumulate(results, lambda val, res: min(val, res)))

print("\nDone!")

from matplotlib import pyplot as plt

fig, ax = plt.subplots()
xAxis = np.arange(1, REPEATS+1, 1)
# f = bestResult[xAxis-1]
ax.set_xlabel('number of iteration', fontsize=18)
ax.set_ylabel('min distance solution', fontsize=18)
ax.legend(loc='upper right', fontsize=18, edgecolor='black')

ax.plot(xAxis, bestResult)
ax.plot(xAxis, [greedyDistance]*REPEATS, label='Greedy Solution')
ax.grid()
plt.show()

print("The average distance is {}.\nStandard deviation is {}.\n".format(
    np.average(results), np.std(results)))

print(stats.ttest_1samp(results, greedyDistance))
