import numpy as np
import cv2
#学習済みのデータを読み込む
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img = cv2.imread('lena.jpg')#イメージデータを読み込む
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える

faces = face_cascade.detectMultiScale(gray, 1.3, 5)#画像の中で顔を探して、その顔の位置の座標を戻す
#カラー画像(img)に、顔を囲む矩形を描画する
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

    eyes = eye_cascade.detectMultiScale(roi_gray)#画像の中で目を探して、その顔の位置の座標を戻す
    #カラー画像(img)に、目を囲む矩形を描画する
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)# フレームを表示する
cv2.waitKey(0)# 0msec待つ
cv2.destroyAllWindows()