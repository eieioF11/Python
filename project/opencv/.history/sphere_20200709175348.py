import cv2
import numpy as np

# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号


while(True):
    frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える   

    #画像左右反転
    frame = cv2.flip(frame, 1)
    gray = cv2.flip(gray, 1)

    cimg = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('frame', cimg)# フレームを表示する

    #キーボードのｑキーが押されたらwhileから抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()