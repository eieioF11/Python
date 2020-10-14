import numpy 
import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (33,33), 1)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 60, param1=10, param2=85, minRadius=10, maxRadius=80)
    if circle is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(frame,(i[0],i[1]),i[2],(255,255,0),2)
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('preview', frame) 
    key = cv2.waitKey(10)
    if key == ord("q"):
        break

cv2.destroyAllWindows()