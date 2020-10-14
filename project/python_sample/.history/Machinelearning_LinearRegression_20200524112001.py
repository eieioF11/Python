import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

X1 = np.random.rand(100,1)

Y = 5 + 3 * X + np.random.rand(100,1)


lin_reg = LinearRegression().fit(X,Y.ravel())

print(lin_reg.intercept_,lin_reg.coef_)

X_new =  np.array([[0],[1]])

plt.plot(X_new,lin_reg.intercept_+lin_reg.coef_*X_new,'red')
plt.scatter(X,Y)
plt.show()