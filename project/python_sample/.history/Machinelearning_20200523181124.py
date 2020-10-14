import numpy as np
import matplotlib.pyplot as plt

X = np.random.rand(100,1)

Y = 5 + 3 * X + np.random.rand(100,1)

plt.scatter(X,Y)
plt.show()