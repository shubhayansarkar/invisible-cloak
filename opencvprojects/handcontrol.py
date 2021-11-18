import numpy as np

from opencvprojects import handrecmodule as ht
import cv2
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
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
    fingers = detector.fing_up()
    frame, img = cap.read()
    img=detector.find_hands(img)
    lm_list=detector.find_position(img,draw=False)
    if len(lm_list) != 0:
        # print(lm_list[4],lm_list[8])
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        fingers = detector.fing_up()
        print(fingers)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    cv2.imshow('1st', img)
    if cv2.waitKey(10) == ord('a'):
        break
cap.release()
cv2.destroyAllWindows()