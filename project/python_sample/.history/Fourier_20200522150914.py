import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10, 10, 0.1)  # x座標を-10 から 10 まで 0.1 きざみで取得
y = np.sin(x)

# グラフを書く
plt.plot(x,y)
# グラフのタイトル
plt.title("price / number")
# x軸のラベル
plt.xlabel("price")
# y軸のラベル
plt.ylabel("number")
# 表示する
plt.show()