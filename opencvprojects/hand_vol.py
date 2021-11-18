import numpy as np

from opencvprojects import handrecmodule as ht
import cv2
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv2.VideoCapture(0)
ptime=0
detector=ht.hand_detector(dic_conf=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
vol_range=(volume.GetVolumeRange())

min_vol=vol_range[0]
max_vol=vol_range[1]
while True:

    frame, img = cap.read()
    img=detector.find_hands(img)
    lm_list=detector.find_position(img,draw=False)

    if len(lm_list)!=0:
       # print(lm_list[4],lm_list[8])
        x1,y1=lm_list[4][1],lm_list[4][2]
        x2,y2=lm_list[8][1],lm_list[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        length=math.hypot((x2-x1),(y2-y1))
        vol =np.interp(length,[10,80],[min_vol,max_vol])
        volume.SetMasterVolumeLevel(vol, None)
        #print(length)
        if length<=30:
           cv2.circle(img, (cx, cy), 7, (0,255, 0), cv2.FILLED)


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    cv2.imshow('1st', img)
    if cv2.waitKey(10) == ord('a'):
        break
cap.release()
cv2.destroyAllWindows()