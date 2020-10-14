import numpy as np
import cv2

img = cv2.imread('lena.jpg')#イメージデータを読み込む
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('image',img)# フレームを表示する
cv2.waitKey(0)# 0msec待つ
cv2.destroyAllWindows()