import numpy as np
import matplotlib.pyplot as plt
from sklearn.liner_model import LinerReg

X = np.random.rand(100,1)

Y = 5 + 3 * X + np.random.rand(100,1)

plt.scatter(X,Y)
plt.show()