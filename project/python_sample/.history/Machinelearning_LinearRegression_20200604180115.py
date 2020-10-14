import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#単回帰
X = np.random.rand(100,1)

w0=5
w1=3

Y = w0 + w1 * X + np.random.rand(100,1)#ノイズをプラス


lin_reg = LinearRegression().fit(X,Y.ravel())

print(lin_reg.intercept_,lin_reg.coef_)

X_new =  np.array([[0],[1]])

plt.plot(X_new,lin_reg.intercept_+lin_reg.coef_*X_new,'red')
plt.scatter(X,Y)
plt.show()

#重回帰

data_size = 20
X = np.linspace(0,1,data)