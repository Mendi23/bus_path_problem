import numpy as np
from matplotlib import pyplot as plt

X = np.array([400,900,390,1000,550])
T = np.linspace(0.01, 5, 100)
alpha = np.min(X)

modifyX = np.frompyfunc(lambda x: (x / alpha) ** (-1 / T), 1, 1)
denuminator = np.sum(modifyX(X))

fig, ax = plt.subplots()
for x in X:
    numerator = modifyX([x])[0]
    P = numerator / denuminator
    ax.plot(T, P, label=x)

ax.set_xlabel('T', fontsize=18)
ax.set_ylabel('P', fontsize=18)
ax.set_title('Probability as a function of the temperature', fontsize=18)
ax.legend(loc='upper right', fontsize=18, edgecolor='black')
ax.set(xbound=(0), ybound=(0)) # dock to left bottom

ax.grid()
plt.show()
