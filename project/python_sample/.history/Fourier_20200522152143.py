import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)  # x座標を-10 から 10 まで 0.1 きざみで取得

k=2

for n in range(1,k,1):
    y=((-1)/(2n-1))np.cos(n*x)
y *= 1/2+2/np.pi


# グラフを書く
plt.plot(x,y)
# グラフのタイトル
plt.title("SIN")
# x軸のラベル
plt.xlabel("x")
# y軸のラベル
plt.ylabel("y")
# 表示する
plt.show()