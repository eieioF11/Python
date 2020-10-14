import numpy as np
import matplotlib.pyplot as plt
import cv2



def F1(k,t):#方形波
    y=0
    for n in range(1,k,1):
        y+=(1/n)*np.sin(np.pi*n/2)*np.cos(n*t)
    y *= 1/2+2/np.pi
    return y

def F2(k,t):#ノコギリ波
    y=0
    for n in range(1,k,1):
        y+=(-1**(n+1)/n)*np.sin(n*t)
    y *= 2
    return y

def F3(k,t):#三角波
    y=np.pi/2
    for n in range(1,k,1):
        y-=(4/np.pi)*(np.cos((2*n-1)*t)/pow(2*n-1,2))
    return y

K=0

plt.title("y=f(t)")# グラフのタイトル
plt.xlabel("t")# x軸のラベル
plt.ylabel("y")# y軸のラベル
X=np.arange(-4*np.pi,4*np.pi, 0.001)

while True:
    K+=1
    Y=F1(K,X)
    print("K=",K)
    plt.plot(Y,label='K='+str(K))# グラフを書く
    plt.text(0,0,'K='+str(K))
    plt.draw()
    plt.pause(0.05)
    plt.cla()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break