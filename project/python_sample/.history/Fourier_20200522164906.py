import numpy as np
import matplotlib.pyplot as plt
import cv2



def F1(k,t):
    y=0
    for n in range(1,k,1):
        y+=(1/n)*np.sin(np.pi*n/2)*np.cos(n*t)
    y *= 1/2+2/np.pi
    return y

def F2(k,t):
    y=0
    for n in range(1,k,1):
        y+=(-1**(n+1)/n)*np.sin(np.pi*n/2)*np.cos(n*t)
    y *= 1/2+2/np.pi
    return y

K=0

plt.title("y=f(t)")# グラフのタイトル
plt.xlabel("t")# x軸のラベル
plt.ylabel("y")# y軸のラベル
X=np.arange(-10, 10, 0.1)

while True:
    K+=1
    Y=F1(K,X)
    print("K=",K)
    plt.plot(Y)# グラフを書く
    plt.draw()
    plt.pause(0.05)
    plt.cla()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break