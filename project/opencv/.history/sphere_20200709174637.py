import cv2
import numpy as np

# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号


while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える   

    #画像左右反転
    frame = cv2.flip(frame, 1)
    gray = cv2.flip(gray, 1)


    cv2.imshow('frame', frame)# フレームを表示する

    #キーボードのｑキーが押されたらwhileから抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()