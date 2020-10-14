import numpy as np
import cv2

img = cv2.imread('lena.jpg')#イメージデータを読み込む
cv2.imshow('image',img)# フレームを表示する
cv2.waitKey(0)# 0msec待つ
cv2.destroyAllWindows()