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
x = np.linspace(0,1,data_size)
noise = np.random.uniform(low=-1.0,high=1.0,size=data_size)*0.2
y=np.sin(2.0 * np.pi*x)+noise
x_line = np.linspace(0,1,1000)
sin_x=np.sin(2.0*np.pi*x_line)


lin_reg = LinearRegression().fit(x.reshape(-1,1),y)
print(lin_reg.intercept_,lin_reg.coef_)
X_2=x**2
x_new=np.concatenate(x.reshape(-1,1),x_2.reshape(-1,1),a)

plt.plot(x_line,sin_x,'red')
plt.scatter(x,y)

plt.show()