import cv2
import time
import numpy as np
lower_black=np.array([201,255,38])
upper_black=np.array([110,255,255])
lower_blue = np.array([101,50,38])
upper_blue = np.array([110,255,255])


cap=cv2.VideoCapture(0)
back=0
time.sleep(3)
for i in range(30):
    ret,back=cap.read(0)



while True:
    frame,img=cap.read()
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    blur=cv2.GaussianBlur(hsv,(35,35),0)
    mask1=cv2.inRange(hsv,lower_black,upper_black)
    mask2=cv2.inRange(hsv,lower_blue,upper_blue)
    
    mask3=mask1+mask2
    mask3=cv2.morphologyEx(mask3,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    img[np.where(mask3==255)]=back[np.where(mask3==255)]
    cv2.imshow('img',img)

    
    if cv2.waitKey(10) == ord('a'):
        break

cap.release()
cv2.destroyAllWindows()
