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
plt.title("SIN")# グラフのタイトル
plt.xlabel("x")# x軸のラベル
plt.ylabel("y")# y軸のラベル

while True:
    pressed_keys = pygame.key.get_pressed() # キー入力を取得
    
    if pressed_keys[K_LEFT]: # ←
        K+=1
        print("left")
        sys.exit()
    if pressed_keys[K_RIGHT]: # →
        print("right")
        K-=1
        sys.exit()
    if pressed_keys[K_UP]: # ↑
        print("up")
        sys.exit()
    if pressed_keys[K_DOWN]: #↓
        print("down")
        sys.exit()
    
    # 以下、別のキー入力取得（ESCキー）
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    X=np.arange(-10, 10, 0.1)
    Y=F(K,X)
    
    plt.plot(X,Y)# グラフを書く
    
    plt.show()# 表示する