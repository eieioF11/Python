import numpy as np
import matplotlib.pyplot as plt

X=.random.read(100,1)

Y = 5 + 3 * X + np.random.read(100,1)
plt.scatter(X,Y)