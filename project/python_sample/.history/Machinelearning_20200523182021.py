import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

X = np.random.rand(100,1)

Y = 5 + 3 * X + np.random.rand(100,1)


lin_reg = LinearRegression().fit(X,Y.ravel())

print(lin_reg.intercept,Line_reg.co)

plt.scatter(X,Y)
plt.show()