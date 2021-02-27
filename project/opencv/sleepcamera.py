import numpy as np
import cv2
import time, datetime
import serial

#Serial
#ser = serial.Serial('/dev/tty.',115200,timeout=None)
#ser = serial.Serial('com6',115200,timeout=None)
# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号
#cap = cv2.VideoCapture(1) # USBカメラ1

ret, frame = cap.read()
grayold = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える
gray = cv2.flip(grayold, 1)

now=time.time()
old=time.time()
start=time.time()

flag1=False
flag2=False
t=0
rem=0
nonrem=0
line=''

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
    
    #rem nonrem time
    if val>0 and not flag1:
        flag1=True
    else:
        if val==0 and flag1:
            now=time.time()
            t=now-old
            flag1=False
            flag2=False
        else:
            if val==0:
                now=time.time()
                nonrem+=now-start
                start=now
    if flag1:
        if not flag2:
            old=time.time()
            flag2=True
            
    #line = ser.readline()
    rem+=t
    t=0
    #send usb serial
    #dispray
    td_rem = datetime.timedelta(seconds=rem)
    td_nonrem = datetime.timedelta(seconds=nonrem)
    print("(rem:"+str(td_rem)+",nonrem:"+str(td_nonrem)+"):"+str(val)+"/"+str(line))
    
    #other
    grayold = gray

    #キーボードのｑキーが押されたらwhileから抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#end processing
#ser.close()
cap.release()# キャプチャを解放する
cv2.destroyAllWindows()
