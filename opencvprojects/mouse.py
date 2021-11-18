import cv2
import numpy as np
import handrecmodule as htm
import time
import pyautogui
import math
##########################
wCam, hCam = 640, 480
frameR = 50 # Frame Reduction
smoothening = 5
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.hand_detector(max_hand=1)
wScr, hScr = pyautogui.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList, bbox = detector.find_position(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1],lmList[8][2]
        x2, y2 = lmList[12][1],lmList[12][2]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fing_up()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0 :
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1 :
            # 9. Find distance between fingers
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[12][1], lmList[12][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
            length = math.hypot((x2 - x1), (y2 - y1))
            # 10. Click mouse if distance short
            if length < 40:
                cv2.circle(img, (cx, cy), 7, (0,255, 0), cv2.FILLED)
                pyautogui.click()
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3]==1and fingers[4]==0:
                pyautogui.press('down')
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3]==1 and fingers[4]==1:
                pyautogui.press('up')

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1)==ord('a'):
        break