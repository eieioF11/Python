import numpy as np
import matplotlib.pyplot as plt

X = np.random(100,1)

Y = 5 + 3 * X + np.random(100,1)

plt.plot(X,Y)
plt.show()