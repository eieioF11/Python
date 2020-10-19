import numpy as np
import cv2
import time
import serial

#Serial
#ser = serial.Serial('/dev/tty.',115200,timeout=None)
# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号

ret, frame = cap.read()
grayold = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える   
gray = cv2.flip(grayold, 1)


while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える   

    #画像左右反転
    frame = cv2.flip(frame, 1)
    gray = cv2.flip(gray, 1)

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(gray)
    fgmask = fgbg.apply(grayold)

    cv2.imshow('frame', frame)# フレームを表示する
    cv2.imshow('fgmask', fgmask)# フレームを表示する

    #白色のピクセル数の算出
    whitePixels = np.count_nonzero(fgmask)

    #黒色のピクセル数の算出
    blackPixels = fgmask.size - whitePixels

    #白色の部分が全体のどれくらいの割合を占めているのかを算出
    val=whitePixels / fgmask.size * 100
    #print(time.time())
    print(val) 

    grayold = gray

    #キーボードのｑキーが押されたらwhileから抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()# キャプチャを解放する
cv2.destroyAllWindows()
