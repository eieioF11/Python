import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import sys


#x = np.arange(-10, 10, 0.1)  # x座標を-10 から 10 まで 0.1 きざみで取得
def F(k,t):
    y=0
    for n in range(1,k,1):
        y+=(1/n)*np.sin(np.pi*n/2)*np.cos(n*t)
    y *= 1/2+2/np.pi
    return y

pygame.init()
screen = pygame.display.set_mode((640, 480))

K=10
X=np.arange(-10, 10, 0.1)
Y=F(K,X)

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