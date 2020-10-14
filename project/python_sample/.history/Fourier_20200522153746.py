import numpy as np
import matplotlib.pyplot as plt

#x = np.arange(-10, 10, 0.1)  # x座標を-10 から 10 まで 0.1 きざみで取得
def F(t)
    k=10
    y=0
    for n in range(1,k,1):
        y+=((-1**n)/(2*n-1))*np.cos(n*t)
    y *= 1/2+2/np.pi
    



# グラフを書く
plt.plot(X,Y)
# グラフのタイトル
plt.title("SIN")
# x軸のラベル
plt.xlabel("x")
# y軸のラベル
plt.ylabel("y")
# 表示する
plt.show()