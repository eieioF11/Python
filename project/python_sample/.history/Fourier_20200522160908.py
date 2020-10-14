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


K=0

plt.title("f(t)")# グラフのタイトル
plt.xlabel("X")# x軸のラベル
plt.ylabel("Y")# y軸のラベル
X=np.arange(-10, 10, 0.1)

while True:
    K+=1
    Y=F(K,X)
    plt.plot(Y)# グラフを書く
    plt.draw()
    plt.pause(0.1)
    plt.cla()
