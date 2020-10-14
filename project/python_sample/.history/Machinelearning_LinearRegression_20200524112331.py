import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

X1 = np.random.rand(100,1)
X2 = np.random.rand(100,1)

Y = 5 + 3 * X1 + 10 * X2 + np.random.rand(100,1)


lin_reg = LinearRegression().fit(X1,Y.ravel())

print(lin_reg.intercept_,lin_reg.coef_)

X1_new =  np.array([[0],[1]])

plt.plot(X1_new,lin_reg.intercept_+lin_reg.coef_*X1_new,'red')
plt.scatter(X1,Y)
plt.show()