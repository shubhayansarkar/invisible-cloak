import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0)
ptime=0
mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils
while True:

    frame, img = cap.read()

    rgbimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(rgbimg)



    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime


    cv2.putText(img,f'FPS:{int(fps)}',(20,40),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),1)
    #print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for mh in result.multi_hand_landmarks:
            for id, lm in enumerate(mh.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if id==4:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
            mpdraw.draw_landmarks(img,mh,mphands.HAND_CONNECTIONS)








    cv2.imshow('1st',img)
    if cv2.waitKey(10) == ord('a'):
        break

cap.release()
cv2.destroyAllWindows()