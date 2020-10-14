import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)  # x座標を-10 から 10 まで 0.1 きざみで取得
y = 1/2+np.sin(x)+10*np.sin(2*x)

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