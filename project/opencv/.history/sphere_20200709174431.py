import cv2
import numpy as np

# カメラをキャプチャする
cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号
img = cv2.imread('opencv_logo.png',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#BGR(青、緑、赤)をRGB(赤、緑、青)の順番に入れ替える   

    #画像左右反転
    frame = cv2.flip(frame, 1)
    gray = cv2.flip(gray, 1)

    # 画像の高さ、幅を取得
    height = frame.shape[0]
    width = frame.shape[1]

    cv2.line(frame, (int(width/2),0), (int(width/2),height), (0,0,0),1)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)#画像の中で顔を探して、その顔の位置の座標を戻す
    #カラー画像(frame)に、顔を囲む矩形を描画する
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        print(x,y)#変数xとyを表示
        cv2.line(frame, (int(width/2),int(height/2)), (int(x+w/2),int(y+h/2)), (0,0,255),3)

        roi_gray = gray[y:y+h, x:x+w]

        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)#画像の中で目を探して、その顔の位置の座標を戻す
        #カラー画像(frame)に、目を囲む矩形を描画する
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


    cv2.imshow('frame', frame)# フレームを表示する

    #キーボードのｑキーが押されたらwhileから抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()